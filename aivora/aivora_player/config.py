"""Shared settings and visual tokens for Aivora V1.0.1."""

import json
import os
import tempfile
from pathlib import Path

APP_NAME = "Aivora"
VERSION = "1.0.1"

# Same base palette as Aivora Studio.
BG = "#101218"
CARD = "#181B22"
CARD_2 = "#20242D"
TEXT = "#F3F4F6"
MUTED = "#9CA3AF"
ACCENT = "#7957FF"
ACCENT_HOVER = "#9278FF"
BORDER = "#303541"

SETTINGS_PATH = Path(
    os.environ.get("APPDATA", Path.home())
) / "Aivora" / "settings.json"
DEFAULT_SETTINGS = {
    "library": "",
    "excluded": "",
    "volume": 0.75,
    "last_track": "",
    "last_position": 0,
    "shuffle": False,
    "repeat": False,
    "favorites": [],
    "playlists": {},
    "recently_played": [],
}


def load_settings():
    """Load local preferences without preventing the player from starting."""
    try:
        stored = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        return normalize_settings(stored)
    except (OSError, json.JSONDecodeError):
        return normalize_settings({})


def normalize_settings(settings):
    """Keep the local settings file valid when it was edited manually."""
    values = {
        **DEFAULT_SETTINGS,
        "favorites": list(DEFAULT_SETTINGS["favorites"]),
        "playlists": dict(DEFAULT_SETTINGS["playlists"]),
        "recently_played": list(DEFAULT_SETTINGS["recently_played"]),
    }
    if isinstance(settings, dict):
        values.update(settings)
    try:
        values["volume"] = max(0.0, min(1.0, float(values.get("volume", 0.75))))
    except (TypeError, ValueError):
        values["volume"] = DEFAULT_SETTINGS["volume"]
    try:
        values["last_position"] = max(0, int(values.get("last_position", 0)))
    except (TypeError, ValueError):
        values["last_position"] = 0
    values["shuffle"] = bool(values.get("shuffle"))
    values["repeat"] = bool(values.get("repeat"))
    favorites = values.get("favorites", [])
    values["favorites"] = [str(path) for path in favorites] if isinstance(favorites, list) else []
    recently_played = values.get("recently_played", [])
    values["recently_played"] = (
        [str(path) for path in recently_played][:20]
        if isinstance(recently_played, list)
        else []
    )
    playlists = values.get("playlists", {})
    values["playlists"] = {
        str(name): [str(path) for path in paths]
        for name, paths in playlists.items()
        if isinstance(paths, list)
    } if isinstance(playlists, dict) else {}
    return values


def save_settings(settings):
    """Persist settings atomically in ``%APPDATA%\\Aivora\\settings.json``."""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=SETTINGS_PATH.parent,
            prefix=".settings-",
            suffix=".json",
            delete=False,
        ) as settings_file:
            json.dump(normalize_settings(settings), settings_file, indent=2, ensure_ascii=False)
            settings_file.write("\n")
            temporary_path = Path(settings_file.name)
        temporary_path.replace(SETTINGS_PATH)
    except OSError:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()
        raise
