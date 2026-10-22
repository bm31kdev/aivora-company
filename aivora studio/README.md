# Aivora Studio V1.0

Aivora Studio est une application Windows en Python/Tkinter pour modifier les
métadonnées audio, gérer les pochettes et organiser les fichiers.

## Installation avec Aivora

Depuis la racine du dépôt, double-cliquez sur
[`Start Aivora Company.bat`](../Start%20Aivora%20Company.bat). Il crée un seul
environnement Python, installe les dépendances partagées, puis lance Aivora et
Aivora Studio V1.0 ensemble.

Python 3 doit être installé et accessible avec `py` ou `python`. Une connexion
Internet est nécessaire seulement lors de la première installation.

## Lancer Studio seul

Après l’installation commune :

```powershell
..\.venv\Scripts\python.exe -m aivora_studio
```

Le fichier [`Start Aivora Studio.bat`](./Start%20Aivora%20Studio.bat) reste
disponible pour installer et lancer uniquement Studio dans son environnement
local.

## Fonctions

- Chargement de fichiers, par sélection ou glisser-déposer.
- Édition de métadonnées et de pochettes.
- Analyse BPM, forme d’onde, conversion et réparation audio.
- Recherche de doublons et rangement dans le dossier du premier artiste.
- Paramètres des dossiers, des fonctions et de la palette visuelle.

Version actuelle : **V1.0**.
