"""Main Tk application composed from focused player modules."""

from .config import APP_NAME, BG, VERSION, load_settings
from .dependencies import tk
from .interface import InterfaceMixin
from .library import LibraryMixin
from .player import PlayerMixin
from .settings import SettingsMixin


class Aivora(InterfaceMixin, LibraryMixin, PlayerMixin, SettingsMixin, tk.Tk):
    """Aivora player assembled with the same mixin architecture as Studio."""

    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} • V{VERSION}")
        self.geometry("1180x720")
        self.minsize(900, 580)
        self.configure(bg=BG)

        self.settings = load_settings()
        self.artists = {}
        self.current_artist = None
        self.current_track = None
        self.is_playing = False
        self.player_ready = False

        self.setup_styles()
        self.build_interface()
        self.after(100, self.scan_library)
