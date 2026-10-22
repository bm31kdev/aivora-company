# Aivora Studio

Aivora Studio est une application Windows pour modifier les métadonnées audio,
gérer les pochettes et organiser les fichiers.

## Installation et lancement

### Installation rapide

Double-clique sur **Start Aivora Studio.bat**. Au premier démarrage, le lanceur
crée un environnement Python isolé, installe si nécessaire les dépendances de
[`requirements.txt`](./requirements.txt), puis démarre l'application. Les
démarrages suivants réutilisent cet environnement sans réinstaller les paquets.

Python 3 doit être installé sur Windows et accessible via `py`, `python` ou
`python3`. Une connexion Internet est nécessaire au premier démarrage pour
télécharger les dépendances.

Si le projet n’est pas encore sur l’ordinateur, le récupérer avec Git :

```powershell
git clone https://github.com/bm31kdev/aivora-studio.git
cd aivora-studio
```

Ensuite, double-clique sur **Start Aivora Studio.bat**. Il crée le dossier
`.venv` et installe les bibliothèques indiquées dans `requirements.txt`.

### Lancement manuel

Pour lancer l'application manuellement après l'installation :

```powershell
.\.venv\Scripts\python.exe -m aivora_studio
```

## Interface actuelle

L’application Tkinter est l’unique interface d’Aivora Studio. Elle permet
d’éditer les métadonnées et les pochettes, d’analyser le BPM, de réparer ou
convertir les fichiers et de les ranger dans le dossier du premier artiste.
Les palettes visuelles se règlent directement dans Paramètres.

La feuille de route des correctifs est dans [`UPDATE.md`](./UPDATE.md).

## Organisation du projet

| Fichier ou dossier | Rôle |
| --- | --- |
| `Start Aivora Studio.bat` | Lanceur Windows : crée l’environnement Python si besoin, installe les dépendances puis démarre l’application. |
| `requirements.txt` | Liste minimale des bibliothèques à installer : glisser-déposer, images, tags audio et FFmpeg. |
| `audio_metadata_editor.py` | Ancien point de lancement, conservé pour compatibilité. |
| `UPDATE.md` | Feuille de route et suivi des correctifs prévus ou livrés. |
| `aivora_studio/__main__.py` | Permet le lancement avec `python -m aivora_studio`. |
| `aivora_studio/main.py` | Point d’entrée Python ; crée et lance la fenêtre. |
| `aivora_studio/app.py` | Assemble la fenêtre et les modules de fonctionnalités. |
| `aivora_studio/interface.py` | Construit l’interface Tkinter : écrans, boutons, styles et fenêtre Versions. |
| `aivora_studio/editor.py` | Charge les fichiers, lit/écrit les métadonnées, renomme et range les sons. |
| `aivora_studio/covers.py` | Lit, affiche, ajoute, remplace et supprime les pochettes. |
| `aivora_studio/audio_tools.py` | Calcule le BPM et la forme d’onde. |
| `aivora_studio/monitoring.py` | Surveille le dossier configuré, convertit et répare les fichiers audio. |
| `aivora_studio/quick_selection.py` | Alimente le rail « Sélection rapide » depuis le dossier exclu. |
| `aivora_studio/duplicates.py` | Recherche les doublons exacts ou audio très similaires. |
| `aivora_studio/artist_folders.py` | Trouve et crée les dossiers des artistes. |
| `aivora_studio/file_operations.py` | Réunit les opérations sûres de copie, déplacement et modification atomique. |
| `aivora_studio/file_locks.py` | Identifie sous Windows l’application qui verrouille un fichier et protège les processus critiques. |
| `aivora_studio/settings.py` | Affiche les paramètres, les palettes, les dossiers et les options activables. |
| `aivora_studio/config.py` | Centralise la version, les couleurs, les chemins et les réglages enregistrés. |
| `aivora_studio/helpers.py` | Fonctions utilitaires, par exemple nettoyage des noms de fichiers et conversion de texte. |
| `aivora_studio/dependencies.py` | Importe les bibliothèques communes pour éviter de les répéter dans chaque module. |
| `aivora_studio/version_history.py` | Données affichées dans la fenêtre Versions. |

Les dossiers `.venv` et `__pycache__` sont générés localement : ils ne doivent
pas être ajoutés à Git.

## Git : committer et pousser sans changer de version

Un **commit** sauvegarde un changement dans Git. Une **version** est le numéro
affiché par l’application. Les deux sont indépendants : tu peux committer et
pousser une correction de texte, de style ou de code sans modifier
`aivora_studio/config.py`, `README.md`, `UPDATE.md` ou `version_history.py`.

Depuis le dossier du projet, vérifie d’abord ce qui a changé :

```powershell
git status
git diff
```

Ajoute seulement les fichiers voulus, crée un commit descriptif, puis envoie-le
sur GitHub :

```powershell
git add aivora_studio/editor.py
git commit -m "Corriger le message d’erreur d’enregistrement"
git push origin main
```

Pour envoyer tous les changements en cours, remplace la première commande par
`git add .`, après avoir vérifié `git status`. Ne change le numéro de version
que pour une vraie livraison : dans ce cas, mets à jour ensemble
`config.py`, `README.md`, `UPDATE.md` et `version_history.py`.

## Fonctions

- Chargement audio par sélection ou glisser-déposer.
- Édition des métadonnées et des pochettes.
- Types `LIVE`, `STUDIO`, `EXTRAIT` et `MAP`, combinables et ajoutés au titre
  et au nom de fichier (ex. `NOM DU SON (LIVE + STUDIO)`). `STUDIO` seul
  conserve le titre et le nom de fichier standard.
- Réparation audio par FFmpeg ; l'original n'est remplacé qu'après validation
  du fichier réparé.
- Conversion en MP3, analyse BPM et surveillance du dossier configuré dans
  `aivora_studio/config.py`.
- Guide et numérotation des versions accessibles en cliquant sur le badge de version.
- Guide des versions : les correctifs suivent la numérotation `1.0.xxx` et
  chaque livraison fait l’objet d’un commit séparé.
- Fenêtre Versions : historique des demandes et changements par version,
  incluant les demandes fonctionnelles initiales avant la remise à zéro en 1.0.
- À l'enregistrement, ranger le fichier dans le dossier du premier artiste et
  créer ce dossier si nécessaire. Les artistes 2+ restent uniquement dans les
  métadonnées.
- Détection des doublons exacts ou audio très similaires ; examiner les
  informations avant de choisir de garder les fichiers ou d'en supprimer un.
- Quatre palettes de couleurs personnalisent l’interface.
- Forme d'onde audio lissée, redessinée en haute résolution avec un dégradé
  doux.
- Fenêtre Paramètres pour personnaliser la palette, les dossiers surveillés
  et l'intervalle de vérification. Les préférences restent sur cet ordinateur.
- Paramètres pour activer ou désactiver séparément le rail de sélection,
  l'édition des pochettes, l'analyse BPM/forme d'onde, la surveillance,
  la conversion, la réparation, le renommage, le contrôle du dossier artiste,
  les types de piste et les majuscules automatiques.
- Option de suppression automatique des métadonnées à l'importation (activée
  par défaut) ; le nom et le contenu audio du fichier sont conservés.
- Vérification après enregistrement : le nom du dossier doit correspondre au
  premier artiste. Les fichiers du dossier exclu et de ses sous-dossiers sont
  ignorés ; un emplacement incorrect affiche un avertissement sans bloquer
  l'enregistrement. Cette vérification peut être désactivée dans les paramètres.
- Typographie cohérente et commandes avec retour visuel au survol et au clavier.
- Rail « Sélection rapide » pour ouvrir les fichiers audio du dossier exclu,
  avec pagination et indication du fichier chargé.

Les paramètres sont enregistrés dans `%APPDATA%\Aivora Studio\settings.json`.

Version actuelle : **1.0**.
