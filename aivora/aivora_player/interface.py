"""Aivora player interface using the Aivora Studio V1.0 layout."""

from .config import ACCENT, ACCENT_HOVER, APP_NAME, BG, BORDER, CARD, CARD_2, MUTED, TEXT, VERSION
from .dependencies import tk, ttk


class InterfaceMixin:
    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Treeview", background=CARD, foreground=TEXT, fieldbackground=CARD,
            rowheight=40, borderwidth=0, font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading", background=CARD, foreground=MUTED,
            relief="flat", font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Treeview", background=[("selected", ACCENT)],
            foreground=[("selected", "#FFFFFF")],
        )

    def build_interface(self):
        """Build the same header, cards and action hierarchy as Studio."""
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 15))

        title_frame = tk.Frame(header, bg=BG)
        title_frame.pack(side="left")
        tk.Label(
            title_frame, text="A", bg=ACCENT, fg="white", font=("Segoe UI", 19, "bold"),
            width=2, height=1,
        ).pack(side="left", padx=(0, 12), pady=(2, 0))
        brand_text = tk.Frame(title_frame, bg=BG)
        brand_text.pack(side="left")
        tk.Label(brand_text, text=APP_NAME, bg=BG, fg=TEXT, font=("Segoe UI", 24, "bold")).pack(anchor="w")
        tk.Label(
            brand_text, text="Bibliothèque et lecteur de musique locale", bg=BG,
            fg=MUTED, font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(2, 0))

        header_actions = tk.Frame(header, bg=BG)
        header_actions.pack(side="right")
        tk.Button(
            header_actions, text="⚙  Paramètres", command=self.show_settings,
            bg=CARD_2, fg=TEXT, activebackground=BORDER, activeforeground=TEXT,
            relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 9, "bold"),
            padx=12, pady=8,
        ).pack(side="right", padx=(8, 0))
        tk.Button(
            header_actions, text=f"V{VERSION}", command=self.show_version,
            bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
            relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 9, "bold"),
            padx=14, pady=8,
        ).pack(side="right")

        overview = tk.Frame(self, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        overview.pack(fill="x", padx=30, pady=(0, 15))
        overview_content = tk.Frame(overview, bg=CARD)
        overview_content.pack(fill="x", padx=16, pady=11)
        tk.Label(
            overview_content, text="LECTEUR AIVORA", bg=CARD, fg=MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left")
        self.library_status = tk.Label(
            overview_content, text="Bibliothèque non analysée", bg=CARD, fg=ACCENT_HOVER,
            font=("Segoe UI", 10, "bold"),
        )
        self.library_status.pack(side="right")
        tk.Label(
            overview_content, text="MP3 • Lecture locale", bg=CARD, fg=MUTED,
            font=("Segoe UI", 8),
        ).pack(side="right", padx=(0, 14))

        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=30, pady=(0, 15))
        tk.Button(
            actions, text="↻  Actualiser la bibliothèque", command=self.scan_library,
            bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
            relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 10, "bold"),
            padx=18, pady=9,
        ).pack(side="left")
        tk.Label(
            actions, text="Choisissez un artiste, puis double-cliquez sur un titre pour le lire.",
            bg=BG, fg=MUTED, font=("Segoe UI", 9),
        ).pack(side="left", padx=(14, 0))

        content = tk.Frame(self, bg=BG)
        content.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        artist_panel = tk.Frame(content, bg=CARD, width=280, highlightbackground=BORDER, highlightthickness=1)
        artist_panel.pack(side="left", fill="both", padx=(0, 10))
        artist_panel.pack_propagate(False)
        tk.Label(artist_panel, text="Bibliothèque", bg=CARD, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(
            anchor="w", padx=20, pady=(18, 3)
        )
        tk.Label(
            artist_panel, text="ARTISTES", bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=20, pady=(12, 8))
        self.artist_list = tk.Listbox(
            artist_panel, bg=CARD_2, fg=TEXT, selectbackground=ACCENT,
            selectforeground="white", activestyle="none", borderwidth=0,
            highlightthickness=0, font=("Segoe UI", 10), exportselection=False,
        )
        self.artist_list.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.artist_list.bind("<<ListboxSelect>>", self.show_artist)

        track_panel = tk.Frame(content, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        track_panel.pack(side="left", fill="both", expand=True)
        track_header = tk.Frame(track_panel, bg=CARD)
        track_header.pack(fill="x", padx=20, pady=(18, 10))
        self.artist_title = tk.Label(
            track_header, text="Chargement de la bibliothèque…", bg=CARD, fg=TEXT,
            font=("Segoe UI", 18, "bold"),
        )
        self.artist_title.pack(anchor="w")
        self.artist_detail = tk.Label(track_header, text="", bg=CARD, fg=MUTED, font=("Segoe UI", 9))
        self.artist_detail.pack(anchor="w", pady=(3, 0))
        table_frame = tk.Frame(track_panel, bg=CARD)
        table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.tracks = ttk.Treeview(
            table_frame, columns=("title", "time", "album"), show="headings", selectmode="browse",
        )
        self.tracks.heading("title", text="TITRE")
        self.tracks.heading("time", text="DURÉE")
        self.tracks.heading("album", text="EMPLACEMENT")
        self.tracks.column("title", width=400, anchor="w")
        self.tracks.column("time", width=90, anchor="center")
        self.tracks.column("album", width=220, anchor="w")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tracks.yview)
        self.tracks.configure(yscrollcommand=scrollbar.set)
        self.tracks.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tracks.bind("<Double-1>", lambda _event: self.play_selected())
        self.tracks.bind("<Return>", lambda _event: self.play_selected())

        player = tk.Frame(self, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        player.pack(fill="x", padx=30, pady=(0, 20))
        player_content = tk.Frame(player, bg=CARD)
        player_content.pack(fill="x", padx=20, pady=14)
        tk.Label(player_content, text="LECTEUR", bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.now_playing = tk.Label(
            player_content, text="Sélectionnez un morceau", bg=CARD, fg=TEXT,
            font=("Segoe UI", 11, "bold"),
        )
        self.now_playing.pack(anchor="w", pady=(3, 0))
        self.player_subtitle = tk.Label(
            player_content, text="Double-cliquez sur un titre pour le lire", bg=CARD,
            fg=MUTED, font=("Segoe UI", 9),
        )
        self.player_subtitle.pack(anchor="w", pady=(2, 0))
        player_actions = tk.Frame(player_content, bg=CARD)
        player_actions.pack(side="right", anchor="e", pady=(0, 20))
        self.stop_btn = tk.Button(
            player_actions, text="■", command=self.stop_playback, bg=CARD_2, fg=TEXT,
            activebackground=BORDER, activeforeground=TEXT, relief="flat", borderwidth=0,
            cursor="hand2", font=("Segoe UI", 12, "bold"), padx=13, pady=8,
        )
        self.stop_btn.pack(side="left", padx=(0, 8))
        self.play_btn = tk.Button(
            player_actions, text="▶", command=self.toggle_play, bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, activeforeground="white", relief="flat",
            borderwidth=0, cursor="hand2", font=("Segoe UI", 14, "bold"), padx=17, pady=7,
        )
        self.play_btn.pack(side="left")
