"""Library indexing, artist pages and release-aware track selection."""

from collections import defaultdict
import re

from .dependencies import MP3, Path, dataclass, threading


@dataclass
class Track:
    path: Path
    title: str
    duration: int = 0
    disc_number: int = 1
    track_number: int = 0
    album: str = ""
    artist: str = ""
    release: str = ""
    release_kind: str = ""


class LibraryMixin:
    ALBUM_MINIMUM_TRACKS = 6

    @staticmethod
    def format_duration(seconds):
        return f"{seconds // 60}:{seconds % 60:02d}" if seconds else "—"

    @classmethod
    def release_kind_for_count(cls, count):
        if count >= cls.ALBUM_MINIMUM_TRACKS:
            return "Album"
        if count == 1:
            return "Single"
        return "Autre sortie"

    def scan_library(self):
        self.artist_title.configure(text="Analyse de la bibliothèque…")
        self.library_status.configure(text="Analyse en cours…")
        self.artist_list.delete(0, "end")
        self.tracks.delete(*self.tracks.get_children())
        self.visible_tracks = []
        self.track_items = {}
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
                tracks = self.read_artist_releases(artist_dir)
                if tracks:
                    found[artist_dir.name] = tracks
        self.after(0, lambda: self.finish_scan(found))

    def read_artist_releases(self, artist_dir):
        """Read each direct child folder as a release on an artist page."""
        releases = []
        try:
            release_dirs = sorted(
                (item for item in artist_dir.iterdir() if item.is_dir()),
                key=lambda item: item.name.lower(),
            )
            loose_tracks = sorted(artist_dir.glob("*.mp3"), key=lambda item: item.name.lower())
        except OSError:
            return releases

        for release_dir in release_dirs:
            try:
                paths = sorted(release_dir.rglob("*.mp3"), key=lambda item: item.name.lower())
            except OSError:
                continue
            releases.extend(self.make_release_tracks(paths, release_dir.name))

        # Keep legacy libraries usable when tracks have not yet been put in a release folder.
        releases.extend(self.make_release_tracks(loose_tracks, "Titres sans dossier"))
        return sorted(
            releases,
            key=lambda track: (track.release.lower(), *self.track_sort_key(track)),
        )

    def make_release_tracks(self, paths, release_name):
        kind = self.release_kind_for_count(len(paths))
        tracks = []
        for path in paths:
            title, duration, album, artist, disc_number, track_number = self.read_track(path)
            tracks.append(
                Track(
                    path=path,
                    title=title,
                    duration=duration,
                    disc_number=disc_number,
                    track_number=track_number,
                    album=album,
                    artist=artist,
                    release=release_name,
                    release_kind=kind,
                )
            )
        return sorted(tracks, key=self.track_sort_key)

    def read_track(self, path):
        title, duration, album, artist, disc_number, track_number = path.stem, 0, "", "", 1, 0
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
                if audio.tags and audio.tags.get("TPOS"):
                    disc_number = self.parse_track_number(audio.tags.get("TPOS")) or 1
                if audio.tags and audio.tags.get("TRCK"):
                    track_number = self.parse_track_number(audio.tags.get("TRCK"))
            except Exception:
                pass
        return title, duration, album, artist, disc_number, track_number

    @staticmethod
    def parse_track_number(value):
        """Return the first numeric value from an ID3 track number such as 03/12."""
        match = re.search(r"\d+", str(value or ""))
        return int(match.group()) if match else 0

    @staticmethod
    def track_sort_key(track):
        """Keep numbered tracks first; retain a stable readable fallback for unnumbered files."""
        return (
            track.disc_number <= 0,
            track.disc_number or 1,
            track.track_number <= 0,
            track.track_number or 0,
            track.title.casefold(),
            track.path.name.casefold(),
        )

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
        """Filter artists by name or by the metadata of their releases."""
        query = self.search_var.get().strip().lower()
        current = self.current_artist
        self.artist_list.delete(0, "end")
        names = []
        for name, tracks in self.artists.items():
            haystack = " ".join(
                [name] + [f"{track.title} {track.album} {track.artist} {track.release}" for track in tracks]
            ).lower()
            if not query or query in haystack:
                names.append(name)
                self.artist_list.insert("end", name)
        if current in names:
            self.artist_list.selection_set(names.index(current))
        return names

    def show_artist(self, _event=None):
        selection = self.artist_list.curselection()
        if not selection:
            return
        self.current_artist = self.artist_list.get(selection[0])
        songs = self.artists[self.current_artist]
        self.current_tracks = songs
        self.update_artist_page_header(songs)
        self.apply_track_filters()

    def update_artist_page_header(self, songs):
        releases = self.group_releases(songs, include_artist=False)
        albums = sum(1 for _, tracks in releases if tracks[0].release_kind == "Album")
        singles = sum(1 for _, tracks in releases if tracks[0].release_kind == "Single")
        other = len(releases) - albums - singles
        summary = [f"{len(songs)} morceau{'x' if len(songs) > 1 else ''}"]
        if albums:
            summary.append(f"{albums} album{'s' if albums > 1 else ''}")
        if singles:
            summary.append(f"{singles} single{'s' if singles > 1 else ''}")
        if other:
            summary.append(f"{other} autre{'s' if other > 1 else ''} sortie{'s' if other > 1 else ''}")
        self.artist_title.configure(text=self.current_artist)
        self.artist_detail.configure(text="  •  ".join(summary))

    def on_search_change(self, *_args):
        names = self.populate_artist_list()
        if names and self.current_artist not in names:
            self.artist_list.selection_set(0)
            self.show_artist()
        else:
            self.apply_track_filters()

    @staticmethod
    def group_releases(tracks, include_artist=True):
        grouped = defaultdict(list)
        for track in tracks:
            key = (track.artist if include_artist else "", track.release, track.release_kind)
            grouped[key].append(track)
        return sorted(
            grouped.items(),
            key=lambda item: (item[0][0].lower(), item[0][1].lower()),
        )

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
            if (not query or query in f"{track.title} {track.album} {track.artist} {track.release}".lower())
            and (allowed_paths is None or str(track.path) in allowed_paths)
        ]
        self.playback_tracks = []
        self.populate_release_tree(show_artist=allowed_paths is not None)
        self.update_track_actions(self.current_track)

    def populate_release_tree(self, show_artist=False):
        self.tracks.delete(*self.tracks.get_children())
        self.track_items = {}
        self.release_items = {}
        for release_index, (release_key, tracks) in enumerate(self.group_releases(self.visible_tracks, show_artist)):
            artist, release, kind = release_key
            prefix = f"{artist}  •  " if artist else ""
            label = f"{prefix}{release or 'Titres sans dossier'}"
            parent_id = f"release-{release_index}"
            total_duration = sum(track.duration for track in tracks)
            cover = self.get_release_cover(tracks)
            self.release_items[parent_id] = tracks
            self.tracks.insert(
                "",
                "end",
                iid=parent_id,
                text=label,
                image=cover or "",
                values=(
                    f"{kind} · {len(tracks)} titre{'s' if len(tracks) > 1 else ''} · {self.format_duration(total_duration)}",
                    "Double-cliquez pour lire",
                    "",
                ),
                open=True,
                tags=("release",),
            )
            for track_index, track in enumerate(tracks):
                item_id = f"track-{release_index}-{track_index}"
                self.track_items[item_id] = track
                number_label = (
                    f"CD {track.disc_number or 1} · {track.track_number:02d}  "
                    if track.track_number else ""
                )
                self.tracks.insert(
                    parent_id,
                    "end",
                    iid=item_id,
                    text=f"{number_label}{track.title}",
                    values=(self.format_duration(track.duration), track.album or kind, "＋ Lire ensuite"),
                    tags=("track",),
                )
        if self.current_track in self.visible_tracks:
            self.select_current_track_in_table()

    def get_selected_track(self):
        selected = self.tracks.selection()
        return self.track_items.get(selected[0]) if selected else None

    def select_track(self, _event=None):
        track = self.get_selected_track()
        if track:
            self.selected_track = track
            if not self.is_playing:
                artist = self.artist_name_for_track(track)
                self.show_cover(track)
                self.track_meta.configure(
                    text=" • ".join(filter(None, (track.artist or artist, track.release or track.album)))
                    or "Métadonnées non disponibles"
                )
            self.update_track_actions(track)

    def queue_tree_track(self, event):
        """Treat the action cell in each track row as a compact queue button."""
        if self.tracks.identify_column(event.x) != "#3":
            return None
        item_id = self.tracks.identify_row(event.y)
        track = self.track_items.get(item_id)
        if track:
            self.enqueue_track(track)
            return "break"
        return None

    def play_tree_item(self, _event=None):
        """Play a track, or start the complete release selected in the tree."""
        selected = self.tracks.selection()
        if not selected:
            return "break"
        release_tracks = self.release_items.get(selected[0])
        if release_tracks:
            self.play_release(release_tracks)
        else:
            self.play_selected()
        return "break"

    def play_release(self, tracks):
        if not tracks:
            return
        self.playback_tracks = list(tracks)
        self.current_track = tracks[0]
        self.current_artist = self.artist_name_for_track(self.current_track)
        self.select_current_track_in_table()
        self.start_playback()

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
                    self.select_current_track_in_table()
                    self.show_cover(track)
                    self.now_playing.configure(text=track.title)
                    self.player_subtitle.configure(text="Dernier morceau prêt à reprendre")
                    self.track_meta.configure(text=f"{artist} • {track.release}")
                    return
