# gpO_TP2# Flask Services — Kanban

Projet de groupe (BUT Informatique 1ère année — TP #2) : quatre microservices web indépendants développés en Python/Flask, gérés avec un tableau Kanban GitHub Projects et un workflow Git en branches.

## Architecture du projet

Le projet est composé de quatre services REST indépendants. Les services 3 et 4 partagent la même base de données MySQL (le Service 4 alimente la base, le Service 3 la lit).

| Service | Responsable | Description | Port |
| --- | --- | --- | --- |
| [`service1_matrices`](./service1_matrices) | Étudiant A | Calculs mathématiques sur matrices (NumPy) | 5001 |
| [`service2_statistiques`](./service2_statistiques) | Étudiant B | Fonctions statistiques sur données JSON (NumPy/SciPy) | 5002 |
| [`service3_stats_mysql`](./service3_stats_mysql) | Étudiant C | Fonctions statistiques depuis MySQL | 5003 |
| [`service4_csv_mysql`](./service4_csv_mysql) | Étudiant D | Chargement d'un CSV vers MySQL | 5004 |

## Structure du dépôt

```
flask-services-kanban/
├── service1_matrices/
│   ├── app.py
│   ├── matrices.py
│   ├── requirements.txt
│   └── README.md
├── service2_statistiques/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── service3_stats_mysql/
│   ├── app.py
│   ├── db.py
│   ├── requirements.txt
│   └── README.md
├── service4_csv_mysql/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── data/
│   └── donnees_exemple.csv
├── sql/
│   └── init_db.sql
├── .gitignore
└── README.md
```

## Installation rapide

Chaque service possède son propre environnement virtuel et son propre `requirements.txt`. Exemple pour un service :

```bash
cd service4_csv_mysql
python -m venv venv
source venv/Scripts/activate    # Windows (Git Bash)
# ou : source venv/bin/activate # Linux/Mac
pip install -r requirements.txt
python app.py
```

Répéter l'opération dans chaque dossier `serviceX_*` pour lancer les quatre services en parallèle (chacun dans son propre terminal).

### Base de données MySQL (Services 3 et 4)

```bash
mysql -u root -p < sql/init_db.sql
```

Chaque service qui se connecte à MySQL nécessite un fichier `.env` local (non versionné) avec :

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=flask_user
DB_PASSWORD=votre_mot_de_passe
DB_NAME=flask_stats
```

## Vue d'ensemble des routes

### Service 1 — Calculs Matriciels (port 5001)

| Méthode | Route | Description |
| --- | --- | --- |
| POST | `/matrices/add` | Addition de deux matrices |
| POST | `/matrices/multiply` | Multiplication de deux matrices |
| POST | `/matrices/transpose` | Transposée d'une matrice |
| POST | `/matrices/determinant` | Déterminant d'une matrice carrée |
| POST | `/matrices/inverse` | Inverse d'une matrice carrée |

```bash
curl -X POST http://localhost:5001/matrices/add \
     -H 'Content-Type: application/json' \
     -d '{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}'
```

### Service 2 — Fonctions Statistiques (port 5002)

| Méthode | Route | Description |
| --- | --- | --- |
| POST | `/stats/describe` | Statistiques descriptives (moyenne, médiane, écart-type, quartiles...) |
| POST | `/stats/correlation` | Corrélation de Pearson entre deux séries |
| POST | `/stats/test_normalite` | Test de normalité de Shapiro-Wilk |
| POST | `/stats/test_student` | Test t de Student (comparaison de deux groupes) |

```bash
curl -X POST http://localhost:5002/stats/describe \
     -H 'Content-Type: application/json' \
     -d '{"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}'
```

### Service 3 — Statistiques depuis MySQL (port 5003)

| Méthode | Route | Description |
| --- | --- | --- |
| GET | `/db/stats/describe?serie=NOM` | Statistiques descriptives d'une série stockée en base |
| GET | `/db/stats/correlation?serie_x=A&serie_y=B` | Corrélation entre deux séries en base |

```bash
curl "http://localhost:5003/db/stats/describe?serie=serie_A"
```

### Service 4 — Chargement CSV vers MySQL (port 5004)

| Méthode | Route | Description |
| --- | --- | --- |
| POST | `/upload/csv` | Charge un fichier CSV (`nom_serie,valeur,categorie,date_mesure`) dans la table `donnees` |
| GET | `/upload/series` | Liste les séries déjà chargées en base avec leur nombre de points |

```bash
curl -X POST http://localhost:5004/upload/csv \
     -F 'file=@data/donnees_exemple.csv'

curl http://localhost:5004/upload/series
```

## Codes HTTP utilisés

| Code | Signification | Cas d'usage |
| --- | --- | --- |
| 200 OK | Succès | Requête traitée, réponse JSON valide |
| 201 Created | Créé | Insertion réussie (ex : CSV chargé dans MySQL) |
| 400 Bad Request | Mauvaise requête | JSON invalide, paramètre manquant, format incorrect |
| 404 Not Found | Non trouvé | Série inexistante dans la base |
| 413 Payload Too Large | Trop volumineux | CSV dépassant la taille maximale autorisée (5 Mo) |
| 500 Internal Server Error | Erreur serveur | Exception non gérée, erreur de connexion BDD |

## Workflow Git & Kanban

- Chaque étudiant développe son service sur une branche dédiée (`feature/sX-...`).
- Une carte du tableau Kanban = une tâche/issue GitHub. WIP limité à 1 carte « En cours » par étudiant.
- Cycle d'une tâche : `À faire` → `En cours` → `En revue` (PR ouverte) → `En test` (PR mergée) → `Terminé`.
- Chaque Pull Request doit être relue et approuvée par un autre membre du groupe avant d'être mergée.
- Le fichier `.env` (identifiants MySQL) ne doit **jamais** être commité — il est listé dans `.gitignore`.

## État d'avancement

- ✅ Partie 1 — Mise en place du projet GitHub & Kanban
- ✅ Partie 2 — Service 1 : Calculs Matriciels
- ✅ Partie 3 — Service 2 : Fonctions Statistiques
- ✅ Partie 4 — Service 3 : Statistiques depuis MySQL
- ✅ Partie 5 — Service 4 : Chargement CSV vers MySQL
- ⬜ Partie 6 — Service 5 : Fonctions C appelées depuis Python (non commencé)