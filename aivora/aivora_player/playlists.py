"""Favorites, recent tracks and user-created local playlists."""

from .config import save_settings
from .dependencies import messagebox, simpledialog


class PlaylistsMixin:
    VIEW_ALL = "Toutes les pistes"
    VIEW_FAVORITES = "★ Favoris"
    VIEW_RECENT = "◷ Récemment écoutés"
    NEW_PLAYLIST = "＋ Nouvelle playlist…"

    def refresh_playlist_menu(self):
        choices = [self.VIEW_ALL, self.VIEW_FAVORITES, self.VIEW_RECENT]
        choices.extend(self.settings["playlists"].keys())
        choices.append(self.NEW_PLAYLIST)
        menu = self.playlist_menu["menu"]
        menu.delete(0, "end")
        for choice in choices:
            menu.add_command(label=choice, command=lambda value=choice: self.set_playlist_view(value))

    def set_playlist_view(self, value):
        if value == self.NEW_PLAYLIST:
            self.create_playlist()
            return
        self.playlist_var.set(value)
        self.apply_track_filters()

    def create_playlist(self):
        name = simpledialog.askstring("Nouvelle playlist", "Nom de la playlist :", parent=self)
        if not name or not name.strip():
            self.playlist_var.set(self.VIEW_ALL)
            return
        name = name.strip()
        if name in self.settings["playlists"]:
            messagebox.showinfo("Playlist existante", "Cette playlist existe déjà.", parent=self)
        else:
            self.settings["playlists"][name] = []
            save_settings(self.settings)
            self.refresh_playlist_menu()
        self.playlist_var.set(name)
        self.apply_track_filters()

    def toggle_favorite(self):
        track = self.get_selected_track()
        if not track:
            return
        path = str(track.path)
        favorites = self.settings["favorites"]
        if path in favorites:
            favorites.remove(path)
        else:
            favorites.append(path)
        save_settings(self.settings)
        self.update_track_actions(track)
        self.apply_track_filters()

    def add_to_playlist(self):
        track = self.get_selected_track()
        playlist = self.playlist_var.get()
        if not track:
            return
        if playlist in (self.VIEW_ALL, self.VIEW_FAVORITES, self.VIEW_RECENT):
            messagebox.showinfo("Choisir une playlist", "Créez ou sélectionnez une playlist avant d’ajouter un titre.", parent=self)
            return
        paths = self.settings["playlists"].setdefault(playlist, [])
        if str(track.path) not in paths:
            paths.append(str(track.path))
            save_settings(self.settings)
        self.apply_track_filters()

    def record_recent_track(self, track):
        path = str(track.path)
        recent = self.settings["recently_played"]
        if path in recent:
            recent.remove(path)
        recent.insert(0, path)
        del recent[20:]
        save_settings(self.settings)

    def update_track_actions(self, track=None):
        track = track or self.get_selected_track()
        if not track:
            self.favorite_btn.configure(text="☆  Favori")
            return
        self.favorite_btn.configure(
            text="★  Retirer des favoris" if str(track.path) in self.settings["favorites"] else "☆  Favori"
        )
