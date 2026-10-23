"""Album-cover extraction and rendering for the player."""

import io

from .dependencies import Image, ImageTk, MP3


class CoverMixin:
    def show_cover(self, track):
        """Display embedded MP3 artwork when available."""
        self.cover_photo = None
        self.cover_label.configure(image="", text="♪")
        if not Image or not ImageTk:
            return
        try:
            audio = MP3(track.path)
            artwork = next(
                (frame.data for frame in audio.tags.values() if frame.FrameID == "APIC"),
                None,
            )
            if not artwork:
                return
            image = Image.open(io.BytesIO(artwork)).convert("RGB")
            image.thumbnail((108, 108))
            self.cover_photo = ImageTk.PhotoImage(image)
            self.cover_label.configure(image=self.cover_photo, text="")
        except Exception:
            return
