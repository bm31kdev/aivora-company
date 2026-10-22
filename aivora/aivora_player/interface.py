"""Aivora player interface, aligned with Aivora Studio visual language."""

from .config import ACCENT, ACCENT_HOVER, APP_NAME, BG, BORDER, CARD, CARD_2, MUTED, TEXT, VERSION
from .dependencies import tk, ttk


class InterfaceMixin:
    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=CARD,
            foreground=TEXT,
            fieldbackground=CARD,
            rowheight=40,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=CARD,
            foreground=MUTED,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", "#FFFFFF")],
        )

    def build_interface(self):
        sidebar = tk.Frame(self, bg=CARD, width=270)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=CARD)
        brand.pack(anchor="w", padx=28, pady=(28, 2))
        tk.Label(
            brand, text="A", bg=ACCENT, fg="white", font=("Segoe UI", 14, "bold"), width=2
        ).pack(side="left", padx=(0, 9))
        tk.Label(brand, text=APP_NAME, bg=CARD, fg=TEXT, font=("Segoe UI", 21, "bold")).pack(side="left")
        tk.Label(
            sidebar, text=f"MUSIQUE LOCALE  •  V{VERSION}", bg=CARD, fg=MUTED, font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=30, pady=(0, 28))

        tk.Label(
            sidebar, text="BIBLIOTHÈQUE", bg=CARD, fg=MUTED, font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=28, pady=(0, 10))
        self.artist_list = tk.Listbox(
            sidebar,
            bg=CARD,
            fg=TEXT,
            selectbackground=ACCENT,
            selectforeground="white",
            activestyle="none",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 11),
            exportselection=False,
        )
        self.artist_list.pack(fill="both", expand=True, padx=16)
        self.artist_list.bind("<<ListboxSelect>>", self.show_artist)

        footer = tk.Frame(sidebar, bg=CARD)
        footer.pack(fill="x", padx=18, pady=22)
        tk.Button(
            footer, text="↻  Actualiser", command=self.scan_library, bg=CARD_2, fg=TEXT,
            activebackground=BORDER, activeforeground=TEXT, relief="flat", padx=12, pady=9, cursor="hand2"
        ).pack(side="left")
        tk.Button(
            footer, text="⚙", command=self.open_settings, bg=CARD_2, fg=TEXT,
            activebackground=BORDER, activeforeground=TEXT, relief="flat", padx=12, pady=9, cursor="hand2"
        ).pack(side="right")
        tk.Button(
            sidebar, text=f"V{VERSION}  •  À propos", command=self.open_about, bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, activeforeground="white", relief="flat", font=("Segoe UI", 9, "bold"),
            cursor="hand2", padx=12, pady=8
        ).pack(anchor="w", padx=20, pady=(0, 14))

        main = tk.Frame(self, bg=BG)
        main.pack(side="left", fill="both", expand=True)
        header = tk.Frame(main, bg=BG)
        header.pack(fill="x", padx=42, pady=(42, 26))
        self.artist_title = tk.Label(
            header, text="Chargement de la bibliothèque…", bg=BG, fg=TEXT, font=("Segoe UI", 27, "bold")
        )
        self.artist_title.pack(anchor="w")
        self.artist_detail = tk.Label(header, text="", bg=BG, fg=MUTED, font=("Segoe UI", 10))
        self.artist_detail.pack(anchor="w", pady=(5, 0))

        table_frame = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        table_frame.pack(fill="both", expand=True, padx=42)
        self.tracks = ttk.Treeview(
            table_frame, columns=("title", "time", "album"), show="headings", selectmode="browse"
        )
        self.tracks.heading("title", text="TITRE")
        self.tracks.heading("time", text="DURÉE")
        self.tracks.heading("album", text="EMPLACEMENT")
        self.tracks.column("title", width=400, anchor="w")
        self.tracks.column("time", width=90, anchor="center")
        self.tracks.column("album", width=260, anchor="w")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tracks.yview)
        self.tracks.configure(yscrollcommand=scrollbar.set)
        self.tracks.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tracks.bind("<Double-1>", lambda _event: self.play_selected())
        self.tracks.bind("<Return>", lambda _event: self.play_selected())

        player = tk.Frame(main, bg=CARD, height=105, highlightbackground=BORDER, highlightthickness=1)
        player.pack(fill="x", side="bottom")
        player.pack_propagate(False)
        self.now_playing = tk.Label(
            player, text="Sélectionnez un morceau", bg=CARD, fg=TEXT, font=("Segoe UI", 11, "bold")
        )
        self.now_playing.place(x=42, y=27)
        self.player_subtitle = tk.Label(
            player, text="Double-cliquez sur un titre pour le lire", bg=CARD, fg=MUTED, font=("Segoe UI", 9)
        )
        self.player_subtitle.place(x=42, y=52)
        self.play_btn = tk.Button(
            player, text="▶", command=self.toggle_play, bg=ACCENT, fg="white", activebackground=ACCENT_HOVER,
            relief="flat", font=("Segoe UI", 16, "bold"), width=4, cursor="hand2"
        )
        self.play_btn.place(relx=1.0, x=-50, y=27, anchor="ne")
