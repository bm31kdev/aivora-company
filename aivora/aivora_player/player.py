"""Playback controls and persisted listening session."""

import random

from .config import ACCENT, ACCENT_HOVER, BG, BORDER, CARD, CARD_2, MUTED, TEXT, save_settings
from .dependencies import messagebox, pygame, tk


class PlayerMixin:
    def queue_selected_track(self):
        """Put the selected library track immediately after the current queue."""
        track = self.get_selected_track()
        if not track:
            messagebox.showinfo("FILE DE LECTURE", "Sélectionnez d’abord un titre à lire ensuite.", parent=self)
            return
        self.enqueue_track(track)

    def enqueue_track(self, track):
        """Append a track to the user-controlled next-up list."""
        if not self.is_playing:
            self.current_track = track
            self.current_artist = self.artist_name_for_track(track)
            self.start_playback()
            return
        if track == self.current_track or track in self.play_queue:
            messagebox.showinfo("FILE DE LECTURE", "Ce titre est déjà en cours ou dans la file.", parent=self)
            return
        self.play_queue.append(track)
        self.update_queue_button()
        self.player_subtitle.configure(text=f"{track.title} sera lu juste après.")

    def update_queue_button(self):
        if hasattr(self, "queue_btn"):
            self.queue_btn.configure(text=f"☷  File ({len(self.play_queue)})")

    def show_play_queue(self):
        dialog = tk.Toplevel(self)
        dialog.title("AIVORA • FILE DE LECTURE")
        dialog.geometry("560x470")
        dialog.minsize(440, 360)
        dialog.configure(bg=BG)
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text="File de lecture", bg=BG, fg=TEXT, font=("Segoe UI", 18, "bold")).pack(
            anchor="w", padx=22, pady=(20, 3)
        )
        tk.Label(
            dialog,
            text="Les titres sont lus dans cet ordre avant la suite normale de l’album ou de la liste.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
            wraplength=500,
            justify="left",
        ).pack(anchor="w", padx=22, pady=(0, 14))

        listbox = tk.Listbox(
            dialog, bg=CARD, fg=TEXT, selectbackground=ACCENT, selectforeground="white",
            activestyle="none", borderwidth=0, highlightthickness=1, highlightbackground=BORDER,
            font=("Segoe UI", 10), exportselection=False,
        )
        listbox.pack(fill="both", expand=True, padx=22)

        def refresh():
            listbox.delete(0, "end")
            for index, track in enumerate(self.play_queue, start=1):
                artist = track.artist or self.artist_name_for_track(track)
                listbox.insert("end", f"{index}.  {track.title}  —  {artist}")
            if not self.play_queue:
                listbox.insert("end", "La file est vide.")
            self.update_queue_button()

        def selected_index():
            selected = listbox.curselection()
            return selected[0] if selected and selected[0] < len(self.play_queue) else None

        def move(offset):
            index = selected_index()
            if index is None:
                return
            destination = index + offset
            if not 0 <= destination < len(self.play_queue):
                return
            self.play_queue[index], self.play_queue[destination] = (
                self.play_queue[destination], self.play_queue[index]
            )
            refresh()
            listbox.selection_set(destination)

        def remove():
            index = selected_index()
            if index is None:
                return
            self.play_queue.pop(index)
            refresh()

        def play_now():
            index = selected_index()
            if index is None:
                return
            self.current_track = self.play_queue.pop(index)
            self.current_artist = self.artist_name_for_track(self.current_track)
            self.update_queue_button()
            self.select_current_track_in_table()
            self.start_playback()
            dialog.destroy()

        controls = tk.Frame(dialog, bg=BG)
        controls.pack(fill="x", padx=22, pady=16)
        button_options = {
            "bg": CARD_2, "fg": TEXT, "activebackground": BORDER, "activeforeground": TEXT,
            "relief": "flat", "borderwidth": 0, "cursor": "hand2", "font": ("Segoe UI", 9, "bold"),
            "padx": 10, "pady": 8,
        }
        tk.Button(controls, text="↑", command=lambda: move(-1), **button_options).pack(side="left")
        tk.Button(controls, text="↓", command=lambda: move(1), **button_options).pack(side="left", padx=(6, 0))
        tk.Button(controls, text="Retirer", command=remove, **button_options).pack(side="left", padx=(10, 0))
        tk.Button(
            controls, text="Lire maintenant", command=play_now, bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, activeforeground="white", relief="flat", borderwidth=0,
            cursor="hand2", font=("Segoe UI", 9, "bold"), padx=10, pady=8,
        ).pack(side="right")
        tk.Button(controls, text="Fermer", command=dialog.destroy, **button_options).pack(side="right", padx=(0, 6))
        refresh()

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
        self.playback_tracks = []
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
            detail = self.playback_error_message(error)
            self.player_subtitle.configure(text=detail)
            messagebox.showerror("Impossible de lire le fichier", f"{detail}\n\nDétail technique : {error}")

    def playback_error_message(self, error):
        path = getattr(self.current_track, "path", None)
        if not path or not path.is_file():
            return "Fichier introuvable : vérifiez que le MP3 n’a pas été déplacé ou supprimé."
        message = str(error).lower()
        if "device" in message or "audio" in message or "mixer" in message:
            return "Le périphérique audio est indisponible : vérifiez la sortie son de Windows."
        if "mp3" in message or "format" in message or "decode" in message:
            return "Ce fichier audio semble corrompu ou dans un format non pris en charge."
        return "Lecture impossible : vérifiez que le fichier est un MP3 lisible."

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
        if direction > 0 and self.play_queue:
            self.current_track = self.play_queue.pop(0)
            self.current_artist = self.artist_name_for_track(self.current_track)
            self.update_queue_button()
            self.select_current_track_in_table()
            self.start_playback()
            return True
        tracks = self.playback_tracks or self.visible_tracks or getattr(self, "current_tracks", [])
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
        volume = max(0.0, min(1.0, float(value)))
        self.volume_var.set(volume)
        if volume > 0:
            self.volume_before_mute = volume
            self.is_muted = False
        if hasattr(self, "mute_btn"):
            self.mute_btn.configure(text="🔊" if not self.is_muted else "🔇")
        if hasattr(self, "volume_label"):
            self.volume_label.configure(text=f"{round(volume * 100)}%")
        if pygame and self.player_ready:
            pygame.mixer.music.set_volume(volume)
        self.save_player_preferences()

    def toggle_mute(self):
        if self.is_muted:
            self.is_muted = False
            self.set_volume(self.volume_before_mute or 0.75)
            return
        current_volume = self.volume_var.get()
        if current_volume > 0:
            self.volume_before_mute = current_volume
        self.is_muted = True
        self.volume_var.set(0)
        if pygame and self.player_ready:
            pygame.mixer.music.set_volume(0)
        self.mute_btn.configure(text="🔇")
        self.volume_label.configure(text="0%")

    def handle_player_shortcut(self, event, action):
        """Global Space/arrow controls while leaving text-entry shortcuts untouched."""
        if isinstance(event.widget, (tk.Entry, tk.Text)):
            return None
        if action == "toggle":
            self.toggle_play()
        elif action == "previous":
            self.play_previous()
        else:
            self.play_next()
        return "break"

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
