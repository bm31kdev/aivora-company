"""Studio-style settings and version-history dialogs for Aivora."""

from .config import (
    ACCENT,
    ACCENT_HOVER,
    APP_NAME,
    BG,
    BORDER,
    CARD,
    CARD_2,
    MUTED,
    TEXT,
    VERSION,
    VERSION_HISTORY,
    save_settings,
)
from .dependencies import filedialog, tk


class SettingsMixin:
    def show_settings(self):
        """Open the Aivora settings dialog using the Studio component style."""
        self.open_settings()

    def open_settings(self):
        dialog = tk.Toplevel(self)
        dialog.title(f"{APP_NAME.upper()} • PARAMÈTRES")
        dialog.configure(bg=BG)
        dialog.geometry("620x470")
        dialog.minsize(500, 380)
        dialog.transient(self)
        dialog.grab_set()

        header = tk.Frame(dialog, bg=BG)
        header.pack(fill="x", padx=24, pady=(20, 14))
        tk.Label(
            header, text="Paramètres", bg=BG, fg=TEXT, font=("Segoe UI", 19, "bold")
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Choisissez la bibliothèque à écouter et le dossier à exclure.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(4, 0))

        _body, content = self.create_scrollable_modal_body(dialog)
        library_card = self.create_settings_section(content, "BIBLIOTHÈQUE AUDIO")
        library_fields = tk.Frame(library_card, bg=CARD)
        library_fields.pack(fill="x", padx=14, pady=(0, 6))
        entries = {
            "excluded": self.create_folder_setting(
                library_fields, "Dossier exclu", self.settings["excluded"], 0
            ),
            "library": self.create_folder_setting(
                library_fields, "Dossier à lire", self.settings["library"], 1
            ),
        }

        preferences_card = self.create_settings_section(content, "PRÉFÉRENCES ENREGISTRÉES")
        tk.Label(
            preferences_card,
            text=(
                "Le volume, les favoris, les playlists, l’historique et la reprise de lecture "
                "sont enregistrés automatiquement dans vos paramètres Aivora."
            ),
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9),
            justify="left",
            anchor="w",
            wraplength=510,
        ).pack(anchor="w", padx=14, pady=(0, 14))

        def apply():
            self.settings.update(
                {key: entry.get().strip() for key, entry in entries.items()}
            )
            save_settings(self.settings)
            dialog.destroy()
            self.scan_library()

        footer = tk.Frame(dialog, bg=BG)
        footer.pack(fill="x", padx=24, pady=18)
        tk.Button(
            footer, text="Annuler", command=dialog.destroy, bg=CARD_2, fg=TEXT,
            activebackground=BORDER, activeforeground=TEXT, relief="flat", borderwidth=0,
            cursor="hand2", font=("Segoe UI", 9, "bold"), padx=14, pady=9,
        ).pack(side="right", padx=(8, 0))
        tk.Button(
            footer, text="Enregistrer", command=apply, bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, activeforeground="white", relief="flat", borderwidth=0,
            cursor="hand2", font=("Segoe UI", 9, "bold"), padx=16, pady=9,
        ).pack(side="right")

    def show_version(self):
        """Open the Studio-style version history from the header."""
        self.show_changelog()

    def show_changelog(self):
        dialog = tk.Toplevel(self)
        dialog.title(f"{APP_NAME} • VERSIONS")
        dialog.configure(bg=BG)
        dialog.geometry("620x560")
        dialog.minsize(500, 420)
        dialog.transient(self)
        dialog.grab_set()

        header = tk.Frame(dialog, bg=BG)
        header.pack(fill="x", padx=24, pady=(22, 16))
        tk.Label(
            header, text="Guide des versions", bg=BG, fg=TEXT, font=("Segoe UI", 19, "bold")
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Fonctionnalités et correctifs livrés dans Aivora.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        _body, history = self.create_scrollable_modal_body(dialog)
        guide = tk.Frame(history, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        guide.pack(fill="x", pady=(0, 12))
        tk.Label(
            guide,
            text="Version installée",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 4))
        tk.Label(
            guide,
            text=f"Aivora V{VERSION} · vos fichiers restent sur votre ordinateur.",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9),
            justify="left",
            anchor="w",
            wraplength=490,
        ).pack(anchor="w", padx=16, pady=(0, 14))

        for version, title, changes in VERSION_HISTORY:
            card = tk.Frame(history, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
            card.pack(fill="x", pady=(0, 12))
            card_header = tk.Frame(card, bg=CARD)
            card_header.pack(fill="x", padx=16, pady=(14, 8))
            tk.Label(
                card_header, text=f"V{version}", bg=ACCENT, fg="white",
                font=("Segoe UI", 8, "bold"), padx=9, pady=4,
            ).pack(side="left")
            tk.Label(
                card_header, text=title, bg=CARD, fg=TEXT, font=("Segoe UI", 11, "bold")
            ).pack(side="left", padx=(10, 0))
            for change in changes:
                row = tk.Frame(card, bg=CARD)
                row.pack(fill="x", padx=16, pady=(0, 9))
                tk.Label(row, text="•", bg=CARD, fg=ACCENT_HOVER, font=("Segoe UI", 12, "bold")).pack(
                    side="left", anchor="n", padx=(0, 8)
                )
                tk.Label(
                    row, text=change, bg=CARD, fg=MUTED, font=("Segoe UI", 9),
                    justify="left", anchor="w", wraplength=490,
                ).pack(side="left", fill="x", expand=True)
        tk.Button(
            dialog, text="Fermer", command=dialog.destroy, bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, activeforeground="white", relief="flat", borderwidth=0,
            cursor="hand2", font=("Segoe UI", 9, "bold"), padx=18, pady=8,
        ).pack(anchor="e", padx=24, pady=18)

    def open_about(self):
        """Backward-compatible alias for the version-history modal."""
        self.show_changelog()

    @staticmethod
    def create_settings_section(parent, title):
        """Create the card component shared by Aivora Studio modals."""
        card = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", pady=(0, 12))
        tk.Label(card, text=title, bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(
            anchor="w", padx=14, pady=(12, 8)
        )
        return card

    def create_folder_setting(self, parent, label, value, row):
        """Use the exact folder-input component used by Aivora Studio."""
        tk.Label(
            parent,
            text=label,
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 8),
        ).grid(row=row * 2, column=0, sticky="w", pady=(6, 3))

        field_row = tk.Frame(parent, bg=CARD)
        field_row.grid(row=row * 2 + 1, column=0, sticky="ew", pady=(0, 8))
        parent.columnconfigure(0, weight=1)

        entry = tk.Entry(
            field_row,
            bg=CARD_2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            font=("Segoe UI", 8),
        )
        entry.insert(0, value)
        entry.pack(side="left", fill="x", expand=True)

        tk.Button(
            field_row,
            text="Parcourir",
            command=lambda: self.browse_setting_folder(entry),
            bg=CARD_2,
            fg=TEXT,
            activebackground=BORDER,
            activeforeground=TEXT,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=("Segoe UI", 8, "bold"),
            padx=10,
            pady=6,
        ).pack(side="left", padx=(8, 0))

        return entry

    @staticmethod
    def browse_setting_folder(entry):
        """Use the same folder-picker behavior as Aivora Studio."""
        selected = filedialog.askdirectory(
            title="CHOISIR UN DOSSIER",
            initialdir=entry.get() or None,
            parent=entry.winfo_toplevel(),
        )
        if selected:
            entry.delete(0, tk.END)
            entry.insert(0, selected)

    @staticmethod
    def create_scrollable_modal_body(dialog):
        """Build the canvas-and-card modal body used by Aivora Studio."""
        body = tk.Frame(dialog, bg=BG)
        body.pack(fill="both", expand=True, padx=24)
        scrollbar = tk.Scrollbar(body, orient="vertical", troughcolor=BG, bg=CARD_2, activebackground=ACCENT)
        scrollbar.pack(side="right", fill="y", padx=(10, 0))
        canvas = tk.Canvas(body, bg=BG, highlightthickness=0, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)
        content = tk.Frame(canvas, bg=BG)
        content_window = canvas.create_window((0, 0), window=content, anchor="nw")
        content.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(content_window, width=event.width))
        return body, content
