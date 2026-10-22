"""Shared settings and visual tokens for Aivora V1.0."""

import json
import os
import tempfile
from pathlib import Path

APP_NAME = "Aivora"
VERSION = "1.0"

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
DEFAULT_SETTINGS = {"library": "", "excluded": ""}


def load_settings():
    """Load local preferences without preventing the player from starting."""
    try:
        stored = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        return {**DEFAULT_SETTINGS, **stored}
    except (OSError, json.JSONDecodeError):
        return DEFAULT_SETTINGS.copy()


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
            json.dump(settings, settings_file, indent=2, ensure_ascii=False)
            settings_file.write("\n")
            temporary_path = Path(settings_file.name)
        temporary_path.replace(SETTINGS_PATH)
    except OSError:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()
        raise
