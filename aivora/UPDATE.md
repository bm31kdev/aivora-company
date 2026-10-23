# Journal des mises à jour — Aivora

## Version 1.0.1 — 23 octobre 2026

- Ajout de la recherche par artiste, titre, album et métadonnée d’artiste.
- Ajout des favoris, playlists locales et de l’historique des 20 derniers titres écoutés.
- Ajout des commandes précédent/suivant, lecture aléatoire, répétition et volume.
- Enchaînement automatique des titres et reprise de la dernière piste à sa position mémorisée.
- Lecture des métadonnées MP3 (titre, album et artiste) et affichage de la pochette intégrée lorsqu’elle existe.
- Les paramètres de bibliothèque n’effacent plus les préférences de lecture, les favoris ou les playlists.

## Version 1.0 — 22 octobre 2026

Première version d’Aivora.

- Bibliothèque de musique locale en Tkinter.
- Analyse des artistes à partir des dossiers directement présents dans la bibliothèque.
- Exclusion configurable d’un dossier.
- Lecture des fichiers MP3 avec pause et reprise.
- Fenêtre des paramètres pour modifier les dossiers indexés.
- Modal « À propos » qui affiche la version installée.
- Les noms d’artistes contenant `&` restent un artiste unique ; les featurings dans le titre n’altèrent pas l’organisation de la discographie.
