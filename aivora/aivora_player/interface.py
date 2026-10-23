"""Aivora player interface using the Aivora Studio-inspired layout."""

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
        style.configure("ArtistPage.Treeview", rowheight=34)

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

        filters = tk.Frame(self, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        filters.pack(fill="x", padx=30, pady=(0, 15))
        tk.Label(filters, text="RECHERCHER", bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(
            side="left", padx=(16, 8), pady=11
        )
        search_entry = tk.Entry(
            filters, textvariable=self.search_var, bg=CARD_2, fg=TEXT, insertbackground=TEXT,
            relief="flat", highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT,
            font=("Segoe UI", 10),
        )
        search_entry.pack(side="left", fill="x", expand=True, pady=8)
        tk.Label(filters, text="LISTE", bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(
            side="left", padx=(16, 8)
        )
        self.playlist_menu = tk.OptionMenu(filters, self.playlist_var, self.VIEW_ALL)
        self.playlist_menu.configure(
            bg=CARD_2, fg=TEXT, activebackground=ACCENT, activeforeground="white",
            relief="flat", borderwidth=0, highlightthickness=0, font=("Segoe UI", 9), padx=9,
        )
        self.playlist_menu["menu"].configure(bg=CARD_2, fg=TEXT, activebackground=ACCENT, activeforeground="white")
        self.playlist_menu.pack(side="left", padx=(0, 16), pady=8)
        self.search_var.trace_add("write", self.on_search_change)
        self.refresh_playlist_menu()

        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=30, pady=(0, 15))
        tk.Button(
            actions, text="↻  Actualiser la bibliothèque", command=self.scan_library,
            bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
            relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 10, "bold"),
            padx=18, pady=9,
        ).pack(side="left")
        self.favorite_btn = tk.Button(
            actions, text="☆  Favori", command=self.toggle_favorite, bg=CARD_2, fg=TEXT,
            activebackground=BORDER, activeforeground=TEXT, relief="flat", borderwidth=0,
            cursor="hand2", font=("Segoe UI", 9, "bold"), padx=12, pady=9,
        )
        self.favorite_btn.pack(side="left", padx=(8, 0))
        tk.Button(
            actions, text="＋ Ajouter à la liste", command=self.add_to_playlist, bg=CARD_2, fg=TEXT,
            activebackground=BORDER, activeforeground=TEXT, relief="flat", borderwidth=0,
            cursor="hand2", font=("Segoe UI", 9, "bold"), padx=12, pady=9,
        ).pack(side="left", padx=(8, 0))
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
            table_frame,
            columns=("duration", "format"),
            show="tree headings",
            selectmode="browse",
            style="ArtistPage.Treeview",
        )
        self.tracks.heading("#0", text="SORTIE / TITRE")
        self.tracks.heading("duration", text="DURÉE / FORMAT")
        self.tracks.heading("format", text="ALBUM")
        self.tracks.column("#0", width=430, anchor="w")
        self.tracks.column("duration", width=155, anchor="center")
        self.tracks.column("format", width=180, anchor="w")
        self.tracks.tag_configure("release", foreground=ACCENT_HOVER, font=("Segoe UI", 10, "bold"))
        self.tracks.tag_configure("track", foreground=TEXT)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tracks.yview)
        self.tracks.configure(yscrollcommand=scrollbar.set)
        self.tracks.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tracks.bind("<Double-1>", lambda _event: self.play_selected())
        self.tracks.bind("<Return>", lambda _event: self.play_selected())
        self.tracks.bind("<<TreeviewSelect>>", self.select_track)

        player = tk.Frame(self, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        player.pack(fill="x", padx=30, pady=(0, 20))
        player_content = tk.Frame(player, bg=CARD)
        player_content.pack(fill="x", padx=20, pady=14)
        self.cover_label = tk.Label(
            player_content, text="♪", bg=CARD_2, fg=ACCENT_HOVER, font=("Segoe UI", 34, "bold"),
            width=5, height=2,
        )
        self.cover_label.pack(side="left", padx=(0, 14))
        player_info = tk.Frame(player_content, bg=CARD)
        player_info.pack(side="left", fill="x", expand=True)
        tk.Label(player_info, text="LECTEUR", bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.now_playing = tk.Label(
            player_info, text="Sélectionnez un morceau", bg=CARD, fg=TEXT,
            font=("Segoe UI", 11, "bold"),
        )
        self.now_playing.pack(anchor="w", pady=(3, 0))
        self.player_subtitle = tk.Label(
            player_info, text="Double-cliquez sur un titre pour le lire", bg=CARD,
            fg=MUTED, font=("Segoe UI", 9),
        )
        self.player_subtitle.pack(anchor="w", pady=(2, 0))
        self.track_meta = tk.Label(player_info, text="", bg=CARD, fg=ACCENT_HOVER, font=("Segoe UI", 8))
        self.track_meta.pack(anchor="w", pady=(2, 0))
        progress_row = tk.Frame(player_info, bg=CARD)
        progress_row.pack(fill="x", pady=(10, 0))
        self.position_label = tk.Label(
            progress_row, text="0:00", bg=CARD, fg=MUTED, font=("Segoe UI", 8), width=5, anchor="w"
        )
        self.position_label.pack(side="left")
        self.progress_scale = tk.Scale(
            progress_row,
            from_=0,
            to=1,
            resolution=1,
            orient="horizontal",
            variable=self.progress_var,
            showvalue=False,
            bg=CARD,
            fg=MUTED,
            troughcolor=CARD_2,
            activebackground=ACCENT,
            highlightthickness=0,
            sliderrelief="flat",
            cursor="hand2",
        )
        self.progress_scale.pack(side="left", fill="x", expand=True, padx=8)
        self.progress_scale.bind("<ButtonPress-1>", self.begin_seek)
        self.progress_scale.bind("<ButtonRelease-1>", self.finish_seek)
        self.duration_label = tk.Label(
            progress_row, text="—", bg=CARD, fg=MUTED, font=("Segoe UI", 8), width=5, anchor="e"
        )
        self.duration_label.pack(side="left")
        player_actions = tk.Frame(player_content, bg=CARD)
        player_actions.pack(side="right", anchor="e", pady=(12, 0))
        self.previous_btn = tk.Button(
            player_actions, text="◀◀", command=self.play_previous, bg=CARD_2, fg=TEXT,
            activebackground=BORDER, activeforeground=TEXT, relief="flat", borderwidth=0,
            cursor="hand2", font=("Segoe UI", 10, "bold"), padx=10, pady=9,
        )
        self.previous_btn.pack(side="left", padx=(0, 8))
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
        self.next_btn = tk.Button(
            player_actions, text="▶▶", command=self.play_next, bg=CARD_2, fg=TEXT,
            activebackground=BORDER, activeforeground=TEXT, relief="flat", borderwidth=0,
            cursor="hand2", font=("Segoe UI", 10, "bold"), padx=10, pady=9,
        )
        self.next_btn.pack(side="left", padx=(8, 0))
        tk.Checkbutton(
            player_actions, text="Aléatoire", variable=self.shuffle_var, command=self.save_player_preferences,
            bg=CARD, fg=MUTED, selectcolor=CARD_2, activebackground=CARD, activeforeground=TEXT,
            font=("Segoe UI", 8),
        ).pack(side="left", padx=(14, 4))
        tk.Checkbutton(
            player_actions, text="Répéter", variable=self.repeat_var, command=self.save_player_preferences,
            bg=CARD, fg=MUTED, selectcolor=CARD_2, activebackground=CARD, activeforeground=TEXT,
            font=("Segoe UI", 8),
        ).pack(side="left")
        tk.Label(player_actions, text="Volume", bg=CARD, fg=MUTED, font=("Segoe UI", 8)).pack(
            side="left", padx=(12, 4)
        )
        tk.Scale(
            player_actions, from_=0, to=1, resolution=0.05, orient="horizontal",
            variable=self.volume_var, command=self.set_volume, showvalue=False, length=76,
            bg=CARD, fg=MUTED, troughcolor=CARD_2, activebackground=ACCENT,
            highlightthickness=0, sliderrelief="flat",
        ).pack(side="left")
