"""Album-cover discovery, caching and rendering for the player."""

import io

from .dependencies import Image, ImageTk, MP3


class CoverMixin:
    COVER_FILENAMES = ("cover.jpg", "cover.jpeg", "cover.png", "folder.jpg", "folder.png", "front.jpg", "front.png")

    def show_cover(self, track):
        """Show an embedded cover first, then a cover image in the release folder."""
        self.cover_photo = None
        self.cover_label.configure(image="", text="♪", width=5, height=2)
        if not Image or not ImageTk:
            return
        cache_key = str(track.path)
        photo = self.cover_cache.get(cache_key)
        if photo is None:
            image = self.load_cover_image(track)
            if image is not None:
                image.thumbnail((120, 120), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.cover_cache[cache_key] = photo
        if photo is not None:
            self.cover_photo = photo
            self.cover_label.configure(image=photo, text="", width=0, height=0)

    def get_release_cover(self, tracks):
        """Return a small cached cover for a release row in the library tree."""
        if not tracks or not Image or not ImageTk:
            return None
        release_key = f"release:{tracks[0].path.parent}"
        photo = self.release_cover_cache.get(release_key)
        if photo is not None:
            return photo
        image = self.load_cover_image(tracks[0])
        if image is None:
            return None
        image.thumbnail((42, 42), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.release_cover_cache[release_key] = photo
        return photo

    def load_cover_image(self, track):
        artwork = self.extract_embedded_artwork(track)
        if artwork:
            try:
                return Image.open(io.BytesIO(artwork)).convert("RGB")
            except Exception:
                pass
        for filename in self.COVER_FILENAMES:
            cover_path = track.path.parent / filename
            if cover_path.is_file():
                try:
                    return Image.open(cover_path).convert("RGB")
                except Exception:
                    continue
        return None

    @staticmethod
    def extract_embedded_artwork(track):
        if not MP3:
            return None
        try:
            audio = MP3(track.path)
            if not audio.tags:
                return None
            for frame in audio.tags.values():
                if getattr(frame, "FrameID", "") == "APIC":
                    return frame.data
        except Exception:
            return None
        return None
