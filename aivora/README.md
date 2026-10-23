# Aivora V1.1.03

Lecteur de musique local en Python/Tkinter. Son environnement et son thème sont alignés avec Aivora Studio V1.0.

Version actuelle : **V1.1.03**.

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

## Nouveautés de V1.1.03

- Lecteur réorganisé : précédent, lecture/pause et suivant sont centrés dans
  la barre, avec les options de lecture et le volume à droite.
- La barre lecteur conserve toujours son espace au bas de la fenêtre et ne
  passe plus sous la bibliothèque.
- Démarrage audio plus robuste grâce à une initialisation de secours du moteur
  de lecture.

## Correctif V1.1.01

- Les pistes d’un album ou d’une sortie sont désormais rangées selon le numéro
  de piste des métadonnées (`TRCK`) : 1, 2, 3… Les fichiers non numérotés
  restent ensuite classés de manière stable.

## Nouveautés de V1.1.0

- Chaque dossier d’artiste affiche une page organisée par dossiers de sortie.
- Un dossier de 6 titres ou plus est affiché comme **Album** ; un dossier d’un titre comme **Single**. Les dossiers de 2 à 5 titres sont conservés en « Autre sortie ».
- Les pochettes sont lues depuis les métadonnées MP3 ou depuis `cover`, `folder` ou `front` en JPG/PNG dans le dossier de sortie.
- Barre de progression, temps écoulé/durée et recherche dans la piste au clic sur le curseur.

## Nouveautés de V1.0.2

- Paramètres, composants de dossier et guide des versions harmonisés avec Aivora Studio.
- Réglages organisés dans AppData selon la même convention qu’Aivora Studio.

## Nouveautés de V1.0.1

- Recherche par artiste, titre, album ou métadonnée d’artiste.
- Lecture du titre précédent/suivant, lecture aléatoire et répétition de la liste affichée.
- Favoris, playlists locales et vue des titres récemment écoutés.
- Réglage du volume et reprise de la dernière piste à sa dernière position.
- Affichage de la pochette embarquée dans les MP3, lorsqu’elle est disponible.
