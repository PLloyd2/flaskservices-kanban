Service 4 — Chargement CSV vers MySQL (Étudiant D)

Description

Ce service est un microservice développé avec Python Flask. Il permet de lire un fichier au format CSV contenant des séries de mesures, de le valider (taille, colonnes, types de données) et de charger son contenu directement dans une base de données commune MySQL (donnees).

Il sert de fournisseur de données pour le Service 3 (Étudiant C).

Fonctionnalités

Vérification de fichier : Validation stricte de l'extension .csv, de la clé file et d'une taille limite maximale de 5 Mo.

Nettoyage automatique : Conversion des types de données, nettoyage des lignes ne contenant pas de valeur numérique valide.

Persistance MySQL : Insertion en masse sécurisée dans la table donnees de votre instance de base de données.

Suivi des séries : Une route GET /upload/series permet de lister instantanément toutes les séries chargées avec leur nombre de points, date de début et de fin.

Installation et Lancement

Préréquis

Avoir un fichier .env configuré à la racine de ce dossier (exclu du suivi Git) contenant les identifiants d'accès à la base de données :

DB_HOST=localhost
DB_USER=votre_utilisateur
DB_PASSWORD=votre_mot_de_passe
DB_NAME=flask_stats


Démarrage du service

Rendez-vous dans le répertoire du service :

cd service4_csv_mysql


Créez et activez votre environnement virtuel :

python -m venv venv
# Sur Windows (PowerShell/CMD) :
.\venv\Scripts\activate
# Sur Linux/Mac :
source venv/bin/activate


Installez les dépendances requises :

pip install -r requirements.txt


Lancez l'application Flask :

python app.py


Le service sera disponible sur le port 5004 (http://localhost:5004).

Spécification des Routes de l'API

1. Charger un fichier CSV : POST /upload/csv

Permet de pousser un fichier CSV et d'insérer les lignes valides en base de données.

Format du fichier CSV attendu :
Le fichier doit comporter au moins les colonnes nom_serie (Texte) et valeur (Nombre). Il peut également inclure categorie (Texte) et date_mesure (Date format YYYY-MM-DD).

Commande de test (curl) :

curl -X POST http://localhost:5004/upload/csv -F "file=@../data/donnees_exemple.csv"


Réponse attendue (201 Created) :

{
  "statut": "success",
  "lignes_inserees": 22,
  "lignes_invalides_ignorees": 0,
  "message": "22 ligne(s) chargée(s) dans la table donnees"
}


Erreurs possibles :

400 Bad Request : Fichier manquant, nom de fichier vide, extension incorrecte ou colonnes obligatoires manquantes.

413 Payload Too Large : Fichier supérieur à 5 Mo.

500 Internal Server Error : Erreur de connexion ou d'écriture dans la base de données MySQL.

2. Lister les séries disponibles : GET /upload/series

Permet d'obtenir un aperçu global de toutes les séries de mesures présentes dans la base de données SQL.

Commande de test (curl) :

curl http://localhost:5004/upload/series


Réponse attendue (200 OK) :

{
  "series": [
    {
      "debut": "2024-01-15",
      "fin": "2024-01-22",
      "n_points": 8,
      "serie": "serie_A"
    },
    {
      "debut": "2024-01-15",
      "fin": "2024-01-22",
      "n_points": 8,
      "serie": "serie_B"
    }
  ],
  "total": 2
}


Erreurs possibles :

500 Internal Server Error : Problème technique ou base de données MySQL inaccessible.