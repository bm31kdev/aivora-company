# Aivora Company — Aivora V1.0.2 & Studio V1.0

Ce dépôt contient les deux applications Python/Tkinter Aivora :

- **Aivora** : lecteur de musique locale.
- **Aivora Studio** : édition de métadonnées, pochettes et organisation de fichiers audio.

## Installer et lancer les deux applications

Sous Windows, double-cliquez sur [Start Aivora Company.bat](./Start%20Aivora%20Company.bat).
Le lanceur crée un unique environnement `.venv`, installe les dépendances
partagées puis ouvre Aivora V1.0.2 et Aivora Studio V1.0.

Python 3 doit être installé et accessible avec `py` ou `python`. Une connexion
Internet est nécessaire uniquement lors de la première installation.

## Lancer une application seule

```powershell
.\.venv\Scripts\python.exe .\aivora\app.py
Set-Location '.\aivora studio'
..\.venv\Scripts\python.exe -m aivora_studio
```
