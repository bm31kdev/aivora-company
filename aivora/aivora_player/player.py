"""Playback controls for the selected library track."""

from .dependencies import messagebox, pygame


class PlayerMixin:
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
            messagebox.showerror(
                "Lecture indisponible",
                "Installez les dépendances avec Start Aivora Company.bat.",
            )
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
            self.player_subtitle.configure(
                text=f"{self.current_artist}  •  {self.current_track.path.name}"
            )
        except Exception as error:
            messagebox.showerror("Impossible de lire le fichier", str(error))

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
