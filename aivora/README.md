# Aivora V1.0.2

Lecteur de musique local en Python/Tkinter. Son environnement et son thème sont alignés avec Aivora Studio V1.0.

Version actuelle : **V1.0.2**.

## Architecture

Le lecteur reprend l’organisation modulaire d’Aivora Studio :

| Module | Responsabilité |
| --- | --- |
| `aivora_player/app.py` | Assemble la fenêtre et les modules de fonctionnalité. |
| `aivora_player/interface.py` | Construit l’interface et les styles partagés avec Studio. |
| `aivora_player/library.py` | Indexe la bibliothèque et affiche les artistes et titres. |
| `aivora_player/player.py` | Gère la lecture, la pause, la reprise et l’enchaînement des titres. |
| `aivora_player/covers.py` | Extrait et affiche les pochettes MP3 intégrées. |
| `aivora_player/playlists.py` | Gère les favoris, l’historique et les playlists locales. |
| `aivora_player/settings.py` | Affiche et enregistre les paramètres et préférences. |
| `aivora_player/config.py` | Centralise la version, le thème et les réglages. |
| `aivora_player/dependencies.py` | Centralise les dépendances communes. |
| `aivora_player/main.py` | Point d’entrée de l’application. |

Les dossiers sélectionnés dans Paramètres sont conservés après fermeture dans
`%APPDATA%\Aivora\settings.json`, avec la même organisation AppData qu’Aivora
Studio et un fichier distinct pour chaque application.
Ce même fichier conserve également le volume, la dernière piste et position de
lecture, les favoris, les playlists et les 20 derniers titres écoutés.

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

## Nouveautés de V1.0.2

- Paramètres, composants de dossier et guide des versions harmonisés avec Aivora Studio.
- Réglages organisés dans AppData selon la même convention qu’Aivora Studio.

## Nouveautés de V1.0.1

- Recherche par artiste, titre, album ou métadonnée d’artiste.
- Lecture du titre précédent/suivant, lecture aléatoire et répétition de la liste affichée.
- Favoris, playlists locales et vue des titres récemment écoutés.
- Réglage du volume et reprise de la dernière piste à sa dernière position.
- Affichage de la pochette embarquée dans les MP3, lorsqu’elle est disponible.
