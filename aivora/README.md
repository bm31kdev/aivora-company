# Aivora V1.0

Lecteur de musique local en Python/Tkinter. Son environnement et son thème sont alignés avec Aivora Studio V1.0.

## Architecture

Le lecteur reprend l’organisation modulaire d’Aivora Studio :

| Module | Responsabilité |
| --- | --- |
| `aivora_player/app.py` | Assemble la fenêtre et les modules de fonctionnalité. |
| `aivora_player/interface.py` | Construit l’interface et les styles partagés avec Studio. |
| `aivora_player/library.py` | Indexe la bibliothèque et affiche les artistes et titres. |
| `aivora_player/player.py` | Gère la lecture, la pause et la reprise. |
| `aivora_player/settings.py` | Affiche et enregistre les paramètres. |
| `aivora_player/config.py` | Centralise la version, le thème et les réglages. |
| `aivora_player/dependencies.py` | Centralise les dépendances communes. |
| `aivora_player/main.py` | Point d’entrée de l’application. |

Depuis la racine du dépôt, double-cliquez sur
[`Start Aivora Company.bat`](../Start%20Aivora%20Company.bat) : il prépare un
environnement Python commun, installe les dépendances des deux applications et
ouvre Aivora ainsi qu’Aivora Studio.

Pour lancer seulement Aivora :

```powershell
..\.venv\Scripts\python.exe app.py
```

Au premier lancement, aucun dossier n’est prérempli. Choisissez le dossier de votre bibliothèque et, si besoin, le dossier à exclure depuis les paramètres.

Chaque dossier situé directement dans la bibliothèque est considéré comme **un seul artiste**, y compris les noms avec un `&` (par exemple `BELLO & DALLAS`). Les crédits dans les titres des MP3 ne modifient jamais cette règle : un morceau `LAGUI & HOOUZ` reste dans la discographie de l'artiste correspondant à son dossier.
