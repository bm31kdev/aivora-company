# Aivora V1.0

Lecteur de musique local en Python/Tkinter. Son environnement et son thème sont alignés avec Aivora Studio V1.0.

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
