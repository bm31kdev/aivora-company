"""Library indexing and artist/track selection."""

from .dependencies import MP3, Path, dataclass, threading


@dataclass
class Track:
    path: Path
    title: str
    duration: int = 0


class LibraryMixin:
    @staticmethod
    def format_duration(seconds):
        return f"{seconds // 60}:{seconds % 60:02d}" if seconds else "—"

    def scan_library(self):
        self.artist_title.configure(text="Analyse de la bibliothèque…")
        self.library_status.configure(text="Analyse en cours…")
        self.artist_list.delete(0, "end")
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
        found = {}
        if root.is_dir():
            for artist_dir in root.iterdir():
                if not artist_dir.is_dir() or (
                    excluded and artist_dir.resolve() == excluded.resolve()
                ):
                    continue
                try:
                    tracks = [
                        Track(path, *self.read_track(path))
                        for path in artist_dir.rglob("*.mp3")
                    ]
                except OSError:
                    continue
                if tracks:
                    found[artist_dir.name] = sorted(
                        tracks, key=lambda track: track.title.lower()
                    )
        self.after(0, lambda: self.finish_scan(found))

    def read_track(self, path):
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
        self.artists = dict(sorted(found.items(), key=lambda item: item[0].lower()))
        for name in self.artists:
            self.artist_list.insert("end", name)
        if self.artists:
            self.library_status.configure(
                text=f"{len(self.artists)} artiste{'s' if len(self.artists) > 1 else ''}"
            )
            self.artist_list.selection_set(0)
            self.show_artist()
        else:
            self.library_status.configure(text="Aucun artiste trouvé")
            self.artist_title.configure(text="Aucun artiste trouvé")
            self.artist_detail.configure(
                text="Choisissez le dossier de votre bibliothèque dans Paramètres."
            )

    def show_artist(self, _event=None):
        selection = self.artist_list.curselection()
        if not selection:
            return
        self.current_artist = self.artist_list.get(selection[0])
        songs = self.artists[self.current_artist]
        self.artist_title.configure(text=self.current_artist)
        self.artist_detail.configure(
            text=f"{len(songs)} morceau{'x' if len(songs) > 1 else ''}  •  Artiste identifié par son dossier"
        )
        self.tracks.delete(*self.tracks.get_children())
        for index, song in enumerate(songs):
            try:
                location = str(
                    song.path.parent.relative_to(
                        Path(self.settings["library"]) / self.current_artist
                    )
                ) or "Singles"
            except ValueError:
                location = song.path.parent.name
            self.tracks.insert(
                "",
                "end",
                iid=str(index),
                values=(song.title, self.format_duration(song.duration), location),
            )
