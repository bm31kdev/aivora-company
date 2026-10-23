"""Centralized optional dependencies used across Aivora modules."""

import threading
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None

try:
    import pygame
except ImportError:
    pygame = None

try:
    from mutagen.mp3 import MP3
except ImportError:
    MP3 = None
