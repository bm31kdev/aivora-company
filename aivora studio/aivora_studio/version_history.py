"""Released versions and the requests they implemented."""

VERSION_HISTORY = (
    (
        "Avant 1.0",
        "Demandes fonctionnelles initiales",
        (
            "Ajouter les types LIVE, STUDIO, EXTRAIT et MAP au titre et au "
            "nom de fichier, autoriser plusieurs types et ne pas suffixer "
            "STUDIO seul.",
            "Investiguer les faux diagnostics de fichiers audio incomplets "
            "et ajouter un outil de réparation audio.",
            "Vérifier que le dossier du fichier correspond au premier artiste, "
            "en ignorant le dossier exclu.",
            "Rendre les fonctionnalités activables individuellement dans les "
            "paramètres et corriger les erreurs de démarrage et de sélection "
            "des types.",
            "Retirer le projet web et conserver uniquement les outils Python.",
        ),
    ),
    (
        "1.0",
        "Nouvelle base Python",
        (
            "Réinitialiser le dépôt et repartir sur une version 1.0 propre.",
            "Conserver uniquement l’application et les outils Python.",
            "Remplacer l’ancien historique par un guide de versionnement.",
        ),
    ),
    (
        "1.0.001",
        "Premier compte à rebours",
        (
            "Ajouter à l’interface un compteur avant la mise à jour prévue "
            "le 9 octobre.",
        ),
    ),
    (
        "1.0.002",
        "Échéance hebdomadaire",
        (
            "Présenter le compte à rebours dans une carte dédiée.",
            "Fixer le rendez-vous des mises à jour au vendredi à 18 h.",
        ),
    ),
    (
        "1.0.003",
        "Personnalisation visuelle",
        (
            "Personnaliser l’interface principale avec un style sombre et un "
            "bouton Enregistrer clair.",
            "Ajouter des palettes réglables et mémoriser les préférences.",
            "Permettre d’ajouter, remplacer et supprimer une pochette.",
            "Afficher la cadence des correctifs et les prochaines versions.",
        ),
    ),
    (
        "1.0.004",
        "Lecture des métadonnées",
        (
            "Charger un fichier depuis le sélecteur ou par glisser-déposer.",
            "Lire artiste, titre, album, artiste album, année, genre, BPM, "
            "piste, compositeur et commentaire dans les champs de l’application.",
            "Reconnaître les types dans le suffixe du titre.",
            "Garder le fichier original intact à l’ouverture ; l’écriture "
            "réelle des tags reste prévue pour une version ultérieure.",
            "Consigner les demandes et changements par version dans les "
            "historique de l’application.",
        ),
    ),
    (
        "1.0.005",
        "Édition et enregistrement",
        (
            "Enregistrer réellement les métadonnées éditées dans les formats "
            "audio pris en charge, sans toucher au fichier avant validation.",
            "Conserver les types multiples dans le titre et le nommage "
            "automatique des fichiers.",
            "Valider BPM et numéro de piste puis afficher les erreurs "
            "d’écriture ou de remplacement sans annoncer un faux succès.",
        ),
    ),
    (
        "1.0.006",
        "Audio et pochettes",
        (
            "Lire, prévisualiser, remplacer et supprimer les pochettes audio ; "
            "ne les intégrer au fichier qu’après Enregistrer.",
            "Remplacer l’onde fictive par une forme d’onde calculée depuis "
            "l’audio décodé par FFmpeg.",
            "Lire et mettre en pause le fichier, déplacer la tête de lecture "
            "et afficher sa durée réelle.",
            "Estimer le BPM depuis le signal audio et l’écrire dans le champ "
            "BPM, prêt à être enregistré avec les autres tags.",
        ),
    ),
    (
        "1.0.007",
        "Rail réel et déplacement après édition",
        (
            "Remplir le rail de sélection depuis le dossier exclu avec scan "
            "asynchrone, pagination, actualisation et erreurs visibles.",
            "Activer par défaut le déplacement après enregistrement pour les "
            "fichiers ouverts depuis ce rail, avec option pour le désactiver.",
            "Choisir le dossier de destination à chaque déplacement, proposer "
            "le dossier surveillé configuré et demander confirmation avant "
            "de remplacer un fichier existant.",
            "Ne supprimer la source du dossier exclu qu’après copie réussie "
            "vers la destination.",
        ),
    ),
    (
        "1.0.008",
        "Déplacement automatique après enregistrement",
        (
            "Déplacer automatiquement vers le dossier LEAK.BM31K tout fichier "
            "enregistré, quelle que soit son origine, dans les interfaces "
            "de l’application.",
            "Conserver les fichiers existants en choisissant automatiquement "
            "un nom disponible en cas de doublon.",
            "Retirer le choix manuel et l’option désactivable de déplacement "
            "de l’application.",
        ),
    ),
    (
        "1.0.009",
        "Palettes visuelles",
        (
            "Proposer dans les paramètres principaux quatre palettes et les "
            "appliquer à l’interface principale.",
        ),
    ),
    (
        "1.0.010",
        "Détection des doublons audio",
        (
            "Détecter les fichiers binaires identiques et les sons très "
            "similaires après réencodage ou légère modification, en combinant "
            "leur spectre audio et la ressemblance de leurs noms/tags.",
            "Demander de vérifier chaque nouveau groupe avec titre, artiste, "
            "album, durée, taille, chemin et score de similarité.",
            "Ne supprimer aucun fichier sans confirmation explicite ; "
            "permettre de garder les deux ou de choisir le fichier à supprimer.",
            "Mettre en cache les empreintes, ignorer le dossier exclu et "
            "signaler clairement les fichiers illisibles.",
        ),
    ),
    (
        "1.0.011",
        "Rangement dans le dossier du premier artiste",
        (
            "Proposer les noms des dossiers artiste existants dans les champs "
            "Artiste de l’application.",
            "Créer le dossier depuis l’outil si le premier artiste n’existe "
            "pas encore.",
            "À l’enregistrement, ranger le fichier uniquement dans le dossier "
            "du premier artiste ; les autres artistes restent dans les tags.",
            "Conserver le déplacement après sauvegarde en évitant d’écraser "
            "les fichiers existants.",
        ),
    ),
    (
        "1.0.012",
        "Suppression des métadonnées à l’importation",
        (
            "Ajouter un réglage pour supprimer automatiquement les "
            "métadonnées lors de l’importation, tout en conservant le nom "
            "et le contenu audio du fichier.",
            "Effectuer la suppression de manière atomique et permettre de "
            "désactiver cette option dans les paramètres.",
        ),
    ),
    (
        "1.0.013",
        "Correction des noms d’artiste avec esperluette",
        (
            "Traiter « & » comme un caractère du nom d’un artiste unique "
            "(par exemple « Bello & Dallas ») au chargement et pour le "
            "choix et la vérification du dossier artiste.",
        ),
    ),
    (
        "1.0.014",
        "Gestion des fichiers verrouillés au renommage",
        (
            "Éviter qu’un fichier audio utilisé par une autre application "
            "fasse apparaître l’enregistrement des métadonnées comme un "
            "échec global.",
            "Conserver le nom existant et avertir clairement l’utilisateur "
            "lorsque Windows refuse le renommage.",
        ),
    ),
    (
        "1.0.015",
        "Respect de la casse du nom à l’importation",
        (
            "Afficher le nom du fichier importé avec sa casse d’origine, "
            "sans appliquer la conversion automatique en majuscules.",
        ),
    ),
    (
        "1.0.016",
        "Déplacement avant renommage",
        (
            "Déplacer le fichier audio vers le dossier du premier artiste "
            "avant d’appliquer le renommage automatique, dans les interfaces "
            "de l’application.",
            "Poursuivre l’enregistrement et conserver le nom existant si le "
            "renommage échoue après le déplacement.",
        ),
    ),
    (
        "1.0.017",
        "Identifier et libérer les fichiers verrouillés",
        (
            "Afficher l’application qui garde un fichier audio ouvert lorsque "
            "Windows bloque son enregistrement, déplacement ou renommage.",
            "Vérifier que le processus n’est pas critique avant de proposer sa "
            "fermeture, puis réessayer seulement après confirmation.",
        ),
    ),
    (
        "1.0",
        "Version 1.0 — interface actuelle unique",
        (
            "Retirer l’ancienne interface alternative et ses dépendances.",
            "Conserver Tkinter comme seule interface et y intégrer les "
            "palettes visuelles.",
        ),
    ),
)
