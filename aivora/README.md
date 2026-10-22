# Aivora V1.0

Lecteur de musique local en Python/Tkinter. Son environnement et son thème sont alignés avec Aivora Studio V1.0.

```powershell
pip install -r requirements.txt
python app.py
```

Au premier lancement, aucun dossier n’est prérempli. Choisissez le dossier de votre bibliothèque et, si besoin, le dossier à exclure depuis les paramètres.

Chaque dossier situé directement dans la bibliothèque est considéré comme **un seul artiste**, y compris les noms avec un `&` (par exemple `BELLO & DALLAS`). Les crédits dans les titres des MP3 ne modifient jamais cette règle : un morceau `LAGUI & HOOUZ` reste dans la discographie de l'artiste correspondant à son dossier.

Les changements sont documentés dans [UPDATE.md](UPDATE.md).
