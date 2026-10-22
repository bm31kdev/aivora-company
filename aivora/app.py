"""Aivora — bibliothèque musicale locale.

Installez la dépendance optionnelle de lecture avec : pip install -r requirements.txt
Puis lancez : python app.py
"""

from __future__ import annotations

import json
import threading
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
    import pygame
except ImportError:  # L'interface et l'indexation restent disponibles.
    pygame = None

try:
    from mutagen.mp3 import MP3
except ImportError:
    MP3 = None


APP_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = APP_DIR / "aivora_settings.json"
APP_VERSION = "1.0"
DEFAULT_LIBRARY = ""
DEFAULT_EXCLUDED = ""

# Palette partagée avec Aivora Studio.
BG = "#101218"
CARD = "#181B22"
CARD_2 = "#20242D"
TEXT = "#F3F4F6"
MUTED = "#9CA3AF"
ACCENT = "#7957FF"
ACCENT_HOVER = "#9278FF"
BORDER = "#303541"


@dataclass
class Track:
    path: Path
    title: str
    duration: int = 0


class Aivora(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Aivora • V{APP_VERSION}")
        self.geometry("1180x720")
        self.minsize(900, 580)
        self.configure(bg=BG)

        self.settings = self.load_settings()
        self.artists: dict[str, list[Track]] = {}
        self.current_artist: str | None = None
        self.current_track: Track | None = None
        self.is_playing = False
        self.player_ready = False
        self.setup_style()
        self.build_ui()
        self.after(100, self.scan_library)

    def load_settings(self):
        defaults = {"library": DEFAULT_LIBRARY, "excluded": DEFAULT_EXCLUDED}
        try:
            return {**defaults, **json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))}
        except (OSError, json.JSONDecodeError):
            return defaults

    def save_settings(self):
        SETTINGS_FILE.write_text(json.dumps(self.settings, indent=2, ensure_ascii=False), encoding="utf-8")

    def setup_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview", background=CARD, foreground=TEXT, fieldbackground=CARD, rowheight=40, borderwidth=0, font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background=CARD, foreground=MUTED, relief="flat", font=("Segoe UI", 9, "bold"))
        s.map("Treeview", background=[("selected", ACCENT)], foreground=[("selected", "#FFFFFF")])
        s.configure("Horizontal.TProgressbar", troughcolor=CARD_2, background=ACCENT, borderwidth=0, thickness=4)

    def build_ui(self):
        sidebar = tk.Frame(self, bg=CARD, width=270)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        brand = tk.Frame(sidebar, bg=CARD)
        brand.pack(anchor="w", padx=28, pady=(28, 2))
        tk.Label(brand, text="A", bg=ACCENT, fg="white", font=("Segoe UI", 14, "bold"), width=2).pack(side="left", padx=(0, 9))
        tk.Label(brand, text="Aivora", bg=CARD, fg=TEXT, font=("Segoe UI", 21, "bold")).pack(side="left")
        tk.Label(sidebar, text=f"MUSIQUE LOCALE  •  V{APP_VERSION}", bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=30, pady=(0, 28))

        tk.Label(sidebar, text="BIBLIOTHÈQUE", bg=CARD, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=28, pady=(0, 10))
        self.artist_list = tk.Listbox(sidebar, bg=CARD, fg=TEXT, selectbackground=ACCENT, selectforeground="#FFFFFF", activestyle="none", borderwidth=0, highlightthickness=0, font=("Segoe UI", 11), exportselection=False)
        self.artist_list.pack(fill="both", expand=True, padx=16)
        self.artist_list.bind("<<ListboxSelect>>", self.show_artist)

        footer = tk.Frame(sidebar, bg=CARD)
        footer.pack(fill="x", padx=18, pady=22)
        tk.Button(footer, text="↻  Actualiser", command=self.scan_library, bg=CARD_2, fg=TEXT, activebackground=BORDER, activeforeground=TEXT, relief="flat", padx=12, pady=9, cursor="hand2").pack(side="left")
        tk.Button(footer, text="⚙", command=self.open_settings, bg=CARD_2, fg=TEXT, activebackground=BORDER, relief="flat", padx=12, pady=9, cursor="hand2").pack(side="right")
        tk.Button(sidebar, text=f"V{APP_VERSION}  •  À propos", command=self.open_about, bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white", relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=12, pady=8).pack(anchor="w", padx=20, pady=(0, 14))

        main = tk.Frame(self, bg=BG)
        main.pack(side="left", fill="both", expand=True)
        header = tk.Frame(main, bg=BG)
        header.pack(fill="x", padx=42, pady=(42, 26))
        self.artist_title = tk.Label(header, text="Chargement de la bibliothèque…", bg=BG, fg=TEXT, font=("Segoe UI", 27, "bold"))
        self.artist_title.pack(anchor="w")
        self.artist_detail = tk.Label(header, text="", bg=BG, fg=MUTED, font=("Segoe UI", 10))
        self.artist_detail.pack(anchor="w", pady=(5, 0))

        table_frame = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        table_frame.pack(fill="both", expand=True, padx=42)
        self.tracks = ttk.Treeview(table_frame, columns=("title", "time", "album"), show="headings", selectmode="browse")
        self.tracks.heading("title", text="TITRE")
        self.tracks.heading("time", text="DURÉE")
        self.tracks.heading("album", text="EMPLACEMENT")
        self.tracks.column("title", width=400, anchor="w")
        self.tracks.column("time", width=90, anchor="center")
        self.tracks.column("album", width=260, anchor="w")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tracks.yview)
        self.tracks.configure(yscrollcommand=scrollbar.set)
        self.tracks.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tracks.bind("<Double-1>", lambda _e: self.play_selected())
        self.tracks.bind("<Return>", lambda _e: self.play_selected())

        player = tk.Frame(main, bg=CARD, height=105, highlightbackground=BORDER, highlightthickness=1)
        player.pack(fill="x", side="bottom")
        player.pack_propagate(False)
        self.now_playing = tk.Label(player, text="Sélectionnez un morceau", bg=CARD, fg=TEXT, font=("Segoe UI", 11, "bold"))
        self.now_playing.place(x=42, y=27)
        self.player_subtitle = tk.Label(player, text="Double-cliquez sur un titre pour le lire", bg=CARD, fg=MUTED, font=("Segoe UI", 9))
        self.player_subtitle.place(x=42, y=52)
        self.play_btn = tk.Button(player, text="▶", command=self.toggle_play, bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, relief="flat", font=("Segoe UI", 16, "bold"), width=4, cursor="hand2")
        self.play_btn.place(relx=1.0, x=-50, y=27, anchor="ne")

    @staticmethod
    def format_duration(seconds: int):
        return f"{seconds // 60}:{seconds % 60:02d}" if seconds else "—"

    def scan_library(self):
        self.artist_title.configure(text="Analyse de la bibliothèque…")
        self.artist_list.delete(0, tk.END)
        self.tracks.delete(*self.tracks.get_children())
        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _scan_worker(self):
        library_path = self.settings["library"].strip()
        excluded_path = self.settings["excluded"].strip()
        if not library_path:
            self.after(0, lambda: self.finish_scan({}))
            return
        root = Path(library_path)
        excluded = Path(excluded_path) if excluded_path else None
        found: dict[str, list[Track]] = {}
        if root.is_dir():
            # Un dossier directement dans la bibliothèque est un artiste. Son nom
            # reste inchangé : « BELLO & DALLAS » est donc un seul artiste.
            for artist_dir in root.iterdir():
                if not artist_dir.is_dir() or (excluded and artist_dir.resolve() == excluded.resolve()):
                    continue
                tracks = []
                try:
                    paths = artist_dir.rglob("*.mp3")
                    for mp3 in paths:
                        title, duration = self.read_track(mp3)
                        tracks.append(Track(mp3, title, duration))
                except OSError:
                    continue
                if tracks:
                    found[artist_dir.name] = sorted(tracks, key=lambda t: t.title.lower())
        self.after(0, lambda: self.finish_scan(found))

    def read_track(self, path: Path):
        title, duration = path.stem, 0
        if MP3:
            try:
                audio = MP3(path)
                duration = int(audio.info.length)
                if audio.tags and audio.tags.get("TIT2"):
                    title = str(audio.tags.get("TIT2"))
            except Exception:
                pass
        return title, duration

    def finish_scan(self, found):
        self.artists = dict(sorted(found.items(), key=lambda pair: pair[0].lower()))
        for name in self.artists:
            self.artist_list.insert(tk.END, name)
        if self.artists:
            self.artist_list.selection_set(0)
            self.show_artist()
        else:
            self.artist_title.configure(text="Aucun artiste trouvé")
            self.artist_detail.configure(text="Vérifiez le dossier de la bibliothèque dans les paramètres.")

    def show_artist(self, _event=None):
        selection = self.artist_list.curselection()
        if not selection:
            return
        self.current_artist = self.artist_list.get(selection[0])
        songs = self.artists[self.current_artist]
        self.artist_title.configure(text=self.current_artist)
        self.artist_detail.configure(text=f"{len(songs)} morceau{'x' if len(songs) > 1 else ''}  •  Artiste identifié par son dossier")
        self.tracks.delete(*self.tracks.get_children())
        for i, song in enumerate(songs):
            try:
                location = str(song.path.parent.relative_to(Path(self.settings["library"]) / self.current_artist)) or "Singles"
            except ValueError:
                location = song.path.parent.name
            self.tracks.insert("", "end", iid=str(i), values=(song.title, self.format_duration(song.duration), location))

    def play_selected(self):
        selected = self.tracks.selection()
        if not selected or not self.current_artist:
            return
        self.current_track = self.artists[self.current_artist][int(selected[0])]
        self.start_playback()

    def start_playback(self):
        if not self.current_track:
            return
        if not pygame:
            messagebox.showerror("Lecture indisponible", "Installez pygame avec la commande :\n\npip install -r requirements.txt")
            return
        try:
            if not self.player_ready:
                pygame.mixer.init()
                self.player_ready = True
            pygame.mixer.music.load(str(self.current_track.path))
            pygame.mixer.music.play()
            self.is_playing = True
            self.play_btn.configure(text="❚❚")
            self.now_playing.configure(text=self.current_track.title)
            self.player_subtitle.configure(text=f"{self.current_artist}  •  {self.current_track.path.name}")
        except Exception as exc:
            messagebox.showerror("Impossible de lire le fichier", str(exc))

    def toggle_play(self):
        if not self.current_track:
            self.play_selected()
            return
        if not pygame or not self.player_ready:
            self.start_playback()
            return
        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_btn.configure(text="▶")
        else:
            pygame.mixer.music.unpause()
            self.play_btn.configure(text="❚❚")
        self.is_playing = not self.is_playing

    def open_settings(self):
        modal = tk.Toplevel(self)
        modal.title("Paramètres")
        modal.configure(bg=BG)
        modal.resizable(False, False)
        modal.transient(self)
        modal.grab_set()
        modal.geometry("690x285")
        tk.Label(modal, text="Paramètres de la bibliothèque", bg=BG, fg=TEXT, font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=28, pady=(25, 20))
        entries = {}
        for key, label in (("excluded", "Dossier exclu"), ("library", "Dossier à prendre")):
            row = tk.Frame(modal, bg=BG)
            row.pack(fill="x", padx=28, pady=7)
            tk.Label(row, text=label, bg=BG, fg=MUTED, width=17, anchor="w", font=("Segoe UI", 10)).pack(side="left")
            value = tk.StringVar(value=self.settings[key])
            entry = tk.Entry(row, textvariable=value, bg=CARD_2, fg=TEXT, insertbackground=TEXT, relief="flat", highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT, font=("Segoe UI", 10))
            entry.pack(side="left", fill="x", expand=True, ipady=7)
            tk.Button(row, text="Parcourir", command=lambda v=value: v.set(filedialog.askdirectory(initialdir=v.get()) or v.get()), bg=CARD_2, fg=TEXT, activebackground=BORDER, activeforeground=TEXT, relief="flat", padx=10).pack(side="left", padx=(8, 0))
            entries[key] = value
        def apply():
            self.settings = {key: field.get().strip() for key, field in entries.items()}
            self.save_settings()
            modal.destroy()
            self.scan_library()
        tk.Button(modal, text="Enregistrer et analyser", command=apply, bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, relief="flat", font=("Segoe UI", 10, "bold"), padx=16, pady=9).pack(anchor="e", padx=28, pady=24)

    def open_about(self):
        modal = tk.Toplevel(self)
        modal.title("À propos d’Aivora")
        modal.configure(bg=BG)
        modal.geometry("420x275")
        modal.resizable(False, False)
        modal.transient(self)
        modal.grab_set()
        tk.Label(modal, text="AIVORA", bg=BG, fg=TEXT, font=("Segoe UI", 25, "bold")).pack(pady=(38, 2))
        tk.Label(modal, text=f"V{APP_VERSION}", bg=BG, fg=ACCENT_HOVER, font=("Segoe UI", 12, "bold")).pack()
        tk.Label(modal, text="Lecteur de musique local", bg=BG, fg=TEXT, font=("Segoe UI", 10)).pack(pady=(18, 4))
        tk.Label(modal, text="Vos fichiers restent sur votre ordinateur.", bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack()
        tk.Button(modal, text="Fermer", command=modal.destroy, bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, relief="flat", font=("Segoe UI", 10, "bold"), padx=24, pady=8).pack(pady=(27, 0))


if __name__ == "__main__":
    Aivora().mainloop()
