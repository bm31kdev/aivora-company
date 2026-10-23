"""Playback controls and persisted listening session."""

import random

from .config import save_settings
from .dependencies import messagebox, pygame


class PlayerMixin:
    def ensure_audio_engine(self):
        """Initialize pygame's mixer, retrying once with a standard audio setup."""
        if not pygame:
            return False
        if self.player_ready:
            return True
        try:
            pygame.mixer.init()
        except pygame.error:
            # A previous failed initialization can leave the mixer half-open.
            # Reset it before trying the standard desktop audio format once.
            pygame.mixer.quit()
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
        self.player_ready = True
        return True

    def play_selected(self):
        track = self.get_selected_track()
        if not track:
            return
        self.current_track = track
        self.current_artist = self.artist_name_for_track(track)
        self.start_playback()

    def start_playback(self, resume=False):
        if not self.current_track:
            return
        if not pygame:
            messagebox.showerror(
                "Lecture indisponible",
                "Installez les dépendances avec Start Aivora Company.bat.",
            )
            return
        try:
            self.ensure_audio_engine()
            pygame.mixer.music.set_volume(self.volume_var.get())
            pygame.mixer.music.load(str(self.current_track.path))
            start_at = self.settings["last_position"] if resume else 0
            if start_at > 0:
                try:
                    pygame.mixer.music.play(start=start_at)
                    self.playback_offset = start_at
                except (TypeError, pygame.error):
                    pygame.mixer.music.play()
                    self.playback_offset = 0
            else:
                pygame.mixer.music.play()
                self.playback_offset = 0
            self.is_playing = True
            self.play_btn.configure(text="❚❚")
            self.now_playing.configure(text=self.current_track.title)
            self.player_subtitle.configure(
                text=f"{self.current_artist}  •  {self.current_track.path.name}"
            )
            self.show_cover(self.current_track)
            self.track_meta.configure(
                text=" • ".join(filter(None, (self.current_track.artist or self.current_artist, self.current_track.album)))
            )
            self.settings["last_track"] = str(self.current_track.path)
            self.settings["last_position"] = 0
            self.playback_position = self.playback_offset
            self.configure_progress(self.current_track.duration, self.playback_position)
            self.record_recent_track(self.current_track)
            self.after(500, self.record_playback_position)
            self.after(500, self.monitor_playback)
        except Exception as error:
            self.is_playing = False
            self.play_btn.configure(text="▶")
            self.player_subtitle.configure(text="Lecture impossible : vérifiez le fichier audio.")
            messagebox.showerror("Impossible de lire le fichier", str(error))

    def toggle_play(self):
        if not self.current_track:
            self.play_selected()
            return
        if not pygame or not self.player_ready:
            self.start_playback(resume=True)
            return
        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_btn.configure(text="▶")
        else:
            pygame.mixer.music.unpause()
            self.play_btn.configure(text="❚❚")
        self.is_playing = not self.is_playing

    def play_next(self):
        self._play_adjacent(1)

    def play_previous(self):
        self._play_adjacent(-1)

    def _play_adjacent(self, direction):
        tracks = self.visible_tracks or getattr(self, "current_tracks", [])
        if not tracks:
            return False
        if self.current_track not in tracks:
            self.current_track = tracks[0]
        elif self.shuffle_var.get() and len(tracks) > 1:
            choices = [track for track in tracks if track != self.current_track]
            self.current_track = random.choice(choices)
        else:
            index = tracks.index(self.current_track) + direction
            if self.repeat_var.get():
                index %= len(tracks)
            elif not 0 <= index < len(tracks):
                return False
            self.current_track = tracks[index]
        self.select_current_track_in_table()
        self.start_playback()
        return True

    def select_current_track_in_table(self):
        if self.current_track not in self.visible_tracks:
            return
        for item_id, track in self.track_items.items():
            if track == self.current_track:
                self.tracks.selection_set(item_id)
                self.tracks.focus(item_id)
                self.tracks.see(item_id)
                return

    def set_volume(self, value):
        self.volume_var.set(float(value))
        if pygame and self.player_ready:
            pygame.mixer.music.set_volume(float(value))
        self.save_player_preferences()

    def save_player_preferences(self):
        self.settings["volume"] = self.volume_var.get()
        self.settings["shuffle"] = self.shuffle_var.get()
        self.settings["repeat"] = self.repeat_var.get()
        save_settings(self.settings)

    def record_playback_position(self):
        if not self.is_playing or not pygame or not self.player_ready:
            return
        position = pygame.mixer.music.get_pos()
        if position >= 0:
            self.playback_position = self.playback_offset + int(position / 1000)
            self.settings["last_position"] = self.playback_position
            self.update_progress_display()
        self.after(500, self.record_playback_position)

    def configure_progress(self, duration, position=0):
        """Configure the scrubber for the selected track."""
        maximum = max(1, duration or 0)
        self.progress_scale.configure(to=maximum, state="normal" if duration else "disabled")
        self.duration_label.configure(text=self.format_duration(duration))
        self.progress_var.set(min(position, maximum))
        self.position_label.configure(text=self.format_duration(position))

    def update_progress_display(self):
        if not self.current_track or self.is_seeking:
            return
        duration = self.current_track.duration
        shown_position = min(self.playback_position, duration) if duration else self.playback_position
        self.progress_var.set(shown_position)
        self.position_label.configure(text=self.format_duration(shown_position))
        self.duration_label.configure(text=self.format_duration(duration))

    def begin_seek(self, _event=None):
        self.is_seeking = True

    def finish_seek(self, _event=None):
        target = int(self.progress_var.get())
        self.is_seeking = False
        if not self.current_track or not pygame or not self.player_ready:
            self.update_progress_display()
            return
        was_playing = self.is_playing
        try:
            pygame.mixer.music.play(start=target)
        except (TypeError, pygame.error):
            self.update_progress_display()
            return
        self.playback_offset = target
        self.playback_position = target
        self.settings["last_position"] = target
        if not was_playing:
            pygame.mixer.music.pause()
        self.update_progress_display()

    def monitor_playback(self):
        """Advance automatically when pygame reaches the end of a track."""
        if not self.is_playing or not pygame or not self.player_ready:
            return
        if pygame.mixer.music.get_busy():
            self.after(500, self.monitor_playback)
            return
        if not self._play_adjacent(1):
            self.stop_playback()

    def stop_playback(self):
        """Stop the player and reset the visible play state."""
        if pygame and self.player_ready:
            pygame.mixer.music.stop()
        self.is_playing = False
        self.playback_position = 0
        self.playback_offset = 0
        self.settings["last_position"] = 0
        self.configure_progress(self.current_track.duration if self.current_track else 0)
        self.play_btn.configure(text="▶")

    def close_app(self):
        if self.current_track:
            self.settings["last_track"] = str(self.current_track.path)
            self.settings["last_position"] = self.playback_position
        self.save_player_preferences()
        if pygame and self.player_ready:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        self.destroy()
