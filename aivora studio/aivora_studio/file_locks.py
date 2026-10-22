"""Windows file-lock diagnostics used before retrying a file operation."""

from __future__ import annotations

import ctypes
import os
from dataclasses import dataclass
from ctypes import wintypes


ERROR_MORE_DATA = 234
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_TERMINATE = 0x0001
RM_APP_TYPE_CRITICAL = 3

# These processes are essential even on older Windows versions where
# ``IsProcessCritical`` is unavailable or cannot inspect the process.
_ESSENTIAL_PROCESS_NAMES = frozenset(
    {
        "csrss.exe",
        "dwm.exe",
        "lsass.exe",
        "services.exe",
        "smss.exe",
        "system",
        "system idle process",
        "wininit.exe",
        "winlogon.exe",
    }
)


@dataclass(frozen=True)
class LockingProcess:
    """A process reported by Windows as using a file."""

    pid: int
    name: str
    safe_to_close: bool
    safety_reason: str = ""


def describe_locking_processes(processes: list[LockingProcess]) -> str:
    """Format a concise French report for the application's two interfaces."""
    if not processes:
        return (
            "Windows n’a pas pu identifier l’application qui utilise ce fichier."
        )
    lines = []
    for process in processes:
        state = "peut être fermé" if process.safe_to_close else "protégé"
        detail = f" — {process.safety_reason}" if process.safety_reason else ""
        lines.append(f"• {process.name} (PID {process.pid}) : {state}{detail}")
    return "\n".join(lines)


def find_locking_processes(path: str) -> list[LockingProcess]:
    """Return processes currently locking *path* on Windows.

    Restart Manager is the Windows-supported way to identify applications that
    prevent a rename, replacement, or deletion.  It returns no result on other
    platforms or when Windows cannot inspect the lock.
    """
    if os.name != "nt" or not path:
        return []

    try:
        return _find_locking_processes_windows(os.path.abspath(path))
    except (AttributeError, OSError):
        return []


def close_locking_process(process: LockingProcess) -> None:
    """Force-close one previously diagnosed, non-critical process.

    This operation is deliberately opt-in from the UI and validates the target
    again immediately before terminating it.
    """
    if os.name != "nt":
        raise OSError("La fermeture d’un processus est disponible sous Windows.")
    if not process.safe_to_close:
        raise PermissionError(process.safety_reason or "Processus protégé.")

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    handle = kernel32.OpenProcess(
        PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_TERMINATE, False, process.pid
    )
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        if _is_process_critical(kernel32, handle):
            raise PermissionError("Windows identifie ce processus comme critique.")
        if not kernel32.TerminateProcess(handle, 1):
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel32.CloseHandle(handle)


def _find_locking_processes_windows(path: str) -> list[LockingProcess]:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    restart_manager = ctypes.WinDLL("Rstrtmgr", use_last_error=True)
    session_handle = wintypes.DWORD()
    session_key = ctypes.create_unicode_buffer(33)
    result = restart_manager.RmStartSession(
        ctypes.byref(session_handle), 0, session_key
    )
    if result:
        raise OSError(result, "Impossible de démarrer le diagnostic Windows.")

    try:
        resources = (wintypes.LPCWSTR * 1)(path)
        result = restart_manager.RmRegisterResources(
            session_handle.value, 1, resources, 0, None, 0, None
        )
        if result:
            raise OSError(result, "Impossible d’inspecter le fichier verrouillé.")

        needed = wintypes.UINT(0)
        count = wintypes.UINT(0)
        reboot_reasons = wintypes.DWORD(0)
        result = restart_manager.RmGetList(
            session_handle.value,
            ctypes.byref(needed),
            ctypes.byref(count),
            None,
            ctypes.byref(reboot_reasons),
        )
        if result not in (0, ERROR_MORE_DATA) or not needed.value:
            return []

        entries = (_RM_PROCESS_INFO * needed.value)()
        count = wintypes.UINT(needed.value)
        result = restart_manager.RmGetList(
            session_handle.value,
            ctypes.byref(needed),
            ctypes.byref(count),
            entries,
            ctypes.byref(reboot_reasons),
        )
        if result:
            raise OSError(result, "Impossible de lire le processus verrouillant.")
        return [_make_locking_process(kernel32, entry) for entry in entries[: count.value]]
    finally:
        restart_manager.RmEndSession(session_handle.value)


class _RM_UNIQUE_PROCESS(ctypes.Structure):
    _fields_ = [("dwProcessId", wintypes.DWORD), ("ProcessStartTime", wintypes.FILETIME)]


class _RM_PROCESS_INFO(ctypes.Structure):
    _fields_ = [
        ("Process", _RM_UNIQUE_PROCESS),
        ("strAppName", wintypes.WCHAR * 256),
        ("strServiceShortName", wintypes.WCHAR * 64),
        ("ApplicationType", wintypes.DWORD),
        ("AppStatus", wintypes.DWORD),
        ("TSSessionId", wintypes.DWORD),
        ("bRestartable", wintypes.BOOL),
    ]


def _make_locking_process(kernel32, entry: _RM_PROCESS_INFO) -> LockingProcess:
    pid = int(entry.Process.dwProcessId)
    name = entry.strAppName.strip() or entry.strServiceShortName.strip() or f"PID {pid}"
    normalized = os.path.basename(name).casefold()
    if pid <= 4 or entry.ApplicationType == RM_APP_TYPE_CRITICAL:
        return LockingProcess(pid, name, False, "Processus système protégé.")
    if normalized in _ESSENTIAL_PROCESS_NAMES:
        return LockingProcess(pid, name, False, "Processus essentiel à Windows.")

    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return LockingProcess(pid, name, False, "Processus non vérifiable : fermeture bloquée.")
    try:
        if _is_process_critical(kernel32, handle):
            return LockingProcess(pid, name, False, "Windows identifie ce processus comme critique.")
    finally:
        kernel32.CloseHandle(handle)
    return LockingProcess(pid, name, True)


def _is_process_critical(kernel32, handle) -> bool:
    try:
        critical = wintypes.BOOL()
        checker = kernel32.IsProcessCritical
        checker.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
        checker.restype = wintypes.BOOL
        return bool(checker(handle, ctypes.byref(critical)) and critical.value)
    except AttributeError:
        return False
