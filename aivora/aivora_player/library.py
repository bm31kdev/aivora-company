"""Library indexing and artist/track selection."""

from .dependencies import MP3, Path, dataclass, threading


@dataclass
class Track:
    path: Path
    title: str
    duration: int = 0
    album: str = ""
    artist: str = ""


class LibraryMixin:
    @staticmethod
    def format_duration(seconds):
        return f"{seconds // 60}:{seconds % 60:02d}" if seconds else "—"

    def scan_library(self):
        self.artist_title.configure(text="Analyse de la bibliothèque…")
        self.library_status.configure(text="Analyse en cours…")
        self.artist_list.delete(0, "end")
        self.tracks.delete(*self.tracks.get_children())
        self.visible_tracks = []
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
        title, duration, album, artist = path.stem, 0, "", ""
        if MP3:
            try:
                audio = MP3(path)
                duration = int(audio.info.length)
                if audio.tags and audio.tags.get("TIT2"):
                    title = str(audio.tags.get("TIT2"))
                if audio.tags and audio.tags.get("TALB"):
                    album = str(audio.tags.get("TALB"))
                if audio.tags and audio.tags.get("TPE1"):
                    artist = str(audio.tags.get("TPE1"))
            except Exception:
                pass
        return title, duration, album, artist

    def finish_scan(self, found):
        self.artists = dict(sorted(found.items(), key=lambda item: item[0].lower()))
        self.populate_artist_list()
        if self.artists:
            self.library_status.configure(
                text=f"{len(self.artists)} artiste{'s' if len(self.artists) > 1 else ''}"
            )
            self.artist_list.selection_set(0)
            self.show_artist()
            self.restore_last_track()
        else:
            self.library_status.configure(text="Aucun artiste trouvé")
            self.artist_title.configure(text="Aucun artiste trouvé")
            self.artist_detail.configure(
                text="Choisissez le dossier de votre bibliothèque dans Paramètres."
            )

    def populate_artist_list(self):
        """Filter artists by name or by the metadata of their tracks."""
        query = self.search_var.get().strip().lower()
        current = self.current_artist
        self.artist_list.delete(0, "end")
        names = []
        for name, tracks in self.artists.items():
            haystack = " ".join(
                [name] + [f"{track.title} {track.album} {track.artist}" for track in tracks]
            ).lower()
            if not query or query in haystack:
                names.append(name)
                self.artist_list.insert("end", name)
        if current in names:
            index = names.index(current)
            self.artist_list.selection_set(index)
        return names

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
        self.current_tracks = songs
        self.apply_track_filters()

    def on_search_change(self, *_args):
        names = self.populate_artist_list()
        if names and self.current_artist not in names:
            self.artist_list.selection_set(0)
            self.show_artist()
        else:
            self.apply_track_filters()

    def apply_track_filters(self):
        songs = getattr(self, "current_tracks", [])
        query = self.search_var.get().strip().lower()
        view = self.playlist_var.get()
        allowed_paths = None
        if view == self.VIEW_FAVORITES:
            allowed_paths = set(self.settings["favorites"])
        elif view == self.VIEW_RECENT:
            allowed_paths = set(self.settings["recently_played"])
        elif view in self.settings["playlists"]:
            allowed_paths = set(self.settings["playlists"][view])
        if allowed_paths is not None:
            songs = [track for tracks in self.artists.values() for track in tracks]
        self.visible_tracks = [
            track for track in songs
            if (not query or query in f"{track.title} {track.album} {track.artist}".lower())
            and (allowed_paths is None or str(track.path) in allowed_paths)
        ]
        self.tracks.delete(*self.tracks.get_children())
        for index, song in enumerate(self.visible_tracks):
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
                values=(song.title, self.format_duration(song.duration), song.album or location),
            )
        if self.current_track in self.visible_tracks:
            self.select_current_track_in_table()
        self.update_track_actions(self.current_track)

    def get_selected_track(self):
        selected = self.tracks.selection()
        if not selected:
            return None
        return self.visible_tracks[int(selected[0])]

    def select_track(self, _event=None):
        track = self.get_selected_track()
        if track:
            self.current_track = track
            self.current_artist = self.artist_name_for_track(track)
            self.show_cover(track)
            self.track_meta.configure(
                text=" • ".join(filter(None, (track.artist or self.current_artist, track.album))) or "Métadonnées non disponibles"
            )
            self.update_track_actions(track)

    def artist_name_for_track(self, track):
        for artist, tracks in self.artists.items():
            if track in tracks:
                return artist
        return self.current_artist or ""

    def restore_last_track(self):
        saved_path = self.settings.get("last_track", "")
        for artist, tracks in self.artists.items():
            for track in tracks:
                if str(track.path) == saved_path:
                    self.current_artist = artist
                    self.populate_artist_list()
                    self.artist_list.selection_set(list(self.artist_list.get(0, "end")).index(artist))
                    self.show_artist()
                    self.current_track = track
                    self.show_cover(track)
                    self.now_playing.configure(text=track.title)
                    self.player_subtitle.configure(text="Dernier morceau prêt à reprendre")
                    return
