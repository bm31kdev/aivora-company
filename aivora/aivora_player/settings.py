"""Settings dialogs and app information."""

from .config import ACCENT, ACCENT_HOVER, BG, BORDER, CARD_2, MUTED, TEXT, VERSION, save_settings
from .dependencies import filedialog, tk


class SettingsMixin:
    def show_settings(self):
        """Studio-style public action used by the header button."""
        self.open_settings()

    def open_settings(self):
        dialog = tk.Toplevel(self)
        dialog.title("Aivora • Paramètres")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.geometry("690x285")

        tk.Label(dialog, text="Paramètres de la bibliothèque", bg=BG, fg=TEXT, font=("Segoe UI", 17, "bold")).pack(
            anchor="w", padx=28, pady=(25, 20)
        )
        entries = {}
        for key, label in (("excluded", "Dossier exclu"), ("library", "Dossier à lire")):
            row = tk.Frame(dialog, bg=BG)
            row.pack(fill="x", padx=28, pady=7)
            tk.Label(row, text=label, bg=BG, fg=MUTED, width=17, anchor="w", font=("Segoe UI", 10)).pack(side="left")
            value = tk.StringVar(value=self.settings[key])
            tk.Entry(
                row, textvariable=value, bg=CARD_2, fg=TEXT, insertbackground=TEXT, relief="flat",
                highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT, font=("Segoe UI", 10)
            ).pack(side="left", fill="x", expand=True, ipady=7)
            tk.Button(
                row, text="Parcourir", command=lambda field=value: field.set(
                    filedialog.askdirectory(initialdir=field.get()) or field.get()
                ), bg=CARD_2, fg=TEXT, activebackground=BORDER, activeforeground=TEXT, relief="flat", padx=10
            ).pack(side="left", padx=(8, 0))
            entries[key] = value

        def apply():
            self.settings.update(
                {key: field.get().strip() for key, field in entries.items()}
            )
            save_settings(self.settings)
            dialog.destroy()
            self.scan_library()

        tk.Button(
            dialog, text="Enregistrer et analyser", command=apply, bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, relief="flat", font=("Segoe UI", 10, "bold"), padx=16, pady=9
        ).pack(anchor="e", padx=28, pady=24)

    def show_version(self):
        """Open the installed-version modal from the header."""
        self.open_about()

    def open_about(self):
        dialog = tk.Toplevel(self)
        dialog.title("À propos d’Aivora")
        dialog.configure(bg=BG)
        dialog.geometry("420x275")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        tk.Label(dialog, text="AIVORA", bg=BG, fg=TEXT, font=("Segoe UI", 25, "bold")).pack(pady=(38, 2))
        tk.Label(dialog, text=f"V{VERSION}", bg=BG, fg=ACCENT_HOVER, font=("Segoe UI", 12, "bold")).pack()
        tk.Label(dialog, text="Lecteur de musique local", bg=BG, fg=TEXT, font=("Segoe UI", 10)).pack(pady=(18, 4))
        tk.Label(dialog, text="Vos fichiers restent sur votre ordinateur.", bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack()
        tk.Button(
            dialog, text="Fermer", command=dialog.destroy, bg=ACCENT, fg="white", activebackground=ACCENT_HOVER,
            relief="flat", font=("Segoe UI", 10, "bold"), padx=24, pady=8
        ).pack(pady=(27, 0))
