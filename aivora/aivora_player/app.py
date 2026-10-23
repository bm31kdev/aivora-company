"""Main Tk application composed from focused player modules."""

from .config import APP_NAME, BG, VERSION, load_settings
from .dependencies import tk
from .covers import CoverMixin
from .interface import InterfaceMixin
from .library import LibraryMixin
from .player import PlayerMixin
from .playlists import PlaylistsMixin
from .settings import SettingsMixin


class Aivora(
    InterfaceMixin,
    LibraryMixin,
    PlayerMixin,
    CoverMixin,
    PlaylistsMixin,
    SettingsMixin,
    tk.Tk,
):
    """Aivora V1.2.0 player assembled with the Studio-style mixin architecture."""

    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} • V{VERSION}")
        self.geometry("1150x850")
        self.minsize(1000, 780)
        self.configure(bg=BG)

        self.settings = load_settings()
        self.artists = {}
        self.current_artist = None
        self.current_track = None
        self.visible_tracks = []
        self.track_items = {}
        self.is_playing = False
        self.player_ready = False
        self.playback_position = 0
        self.playback_offset = 0
        self.is_seeking = False
        self.search_var = tk.StringVar()
        self.playlist_var = tk.StringVar(value=self.VIEW_ALL)
        self.volume_var = tk.DoubleVar(value=self.settings["volume"])
        self.shuffle_var = tk.BooleanVar(value=self.settings["shuffle"])
        self.repeat_var = tk.BooleanVar(value=self.settings["repeat"])
        self.progress_var = tk.DoubleVar(value=0)
        self.cover_photo = None
        self.cover_cache = {}

        self.setup_styles()
        self.build_interface()
        self.configure_progress(0)
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.after(100, self.scan_library)
