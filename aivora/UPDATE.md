# Journal des mises à jour — Aivora

## Version 1.1.01 — 23 octobre 2026

- Les titres d’album et de sortie sont classés selon leur numéro de piste
  dans les métadonnées (`TRCK`) : la piste 1 apparaît en premier.
- Les fichiers sans numéro de piste sont conservés après les pistes numérotées.

## Version 1.1.0 — 23 octobre 2026

- Page d’artiste organisée par dossiers de sortie, avec les pistes dépliables sous chaque sortie.
- Un dossier de plus de 5 titres est classé Album ; un dossier d’un titre est classé Single.
- Les dossiers de 2 à 5 titres restent disponibles sous « Autre sortie ».
- Pochettes intégrées ou fichiers `cover`, `folder` et `front` dans le dossier de la sortie.
- Barre de progression avec temps écoulé, durée et recherche dans la lecture.

## Version 1.0.2 — 23 octobre 2026

- Stockage des réglages aligné sur la convention AppData d’Aivora Studio.
- Modal Paramètres réutilise les composants de dossier, cartes et actions de Studio.
- Guide des versions avec historique et défilement aligné sur le modal Studio.

## Version 1.0.1 — 23 octobre 2026

- Ajout de la recherche par artiste, titre, album et métadonnée d’artiste.
- Ajout des favoris, playlists locales et de l’historique des 20 derniers titres écoutés.
- Ajout des commandes précédent/suivant, lecture aléatoire, répétition et volume.
- Enchaînement automatique des titres et reprise de la dernière piste à sa position mémorisée.
- Lecture des métadonnées MP3 (titre, album et artiste) et affichage de la pochette intégrée lorsqu’elle existe.
- Les paramètres de bibliothèque n’effacent plus les préférences de lecture, les favoris ou les playlists.
- Paramètres et historique des versions alignés sur les composants de modal d’Aivora Studio.

## Version 1.0 — 22 octobre 2026

Première version d’Aivora.

- Bibliothèque de musique locale en Tkinter.
- Analyse des artistes à partir des dossiers directement présents dans la bibliothèque.
- Exclusion configurable d’un dossier.
- Lecture des fichiers MP3 avec pause et reprise.
- Fenêtre des paramètres pour modifier les dossiers indexés.
- Modal « À propos » qui affiche la version installée.
- Les noms d’artistes contenant `&` restent un artiste unique ; les featurings dans le titre n’altèrent pas l’organisation de la discographie.
