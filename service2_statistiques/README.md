# Service 2 — Statistiques JSON

API REST Flask pour effectuer des calculs statistiques sur des données JSON.

## Prérequis

- Python 3.x
- pip

## Installation

```bash
cd service2_statistiques
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Lancement du serveur

```bash
python app.py
```

Le serveur tourne sur http://localhost:5002

## Routes disponibles

### POST /stats/describe
Calcule les statistiques descriptives d'un tableau de valeurs.

**Corps :** `{"data": [12.5, 15.3, 8.7, 21.0]}`

**Réponse 200 :**
```json
{
  "operation": "description",
  "resultat": {
    "n": 4, "moyenne": 15.25, "mediane": 13.9,
    "ecart_type": 3.69, "variance": 13.6,
    "minimum": 8.7, "maximum": 21.0,
    "q1": 11.0, "q3": 15.875, "etendue": 12.3
  }
}
```

### POST /stats/correlation
Calcule le coefficient de corrélation de Pearson entre deux séries.

**Corps :** `{"x": [1,2,3,4,5], "y": [2,4,5,4,5]}`

**Réponse 200 :**
```json
{
  "operation": "correlation_pearson",
  "resultat": {
    "r": 0.7746, "p_value": 0.124,
    "interpretation": "forte", "significatif": false
  }
}
```

### POST /stats/test_normalite
Test de Shapiro-Wilk pour vérifier si une distribution est normale.

**Corps :** `{"data": [12.5, 15.3, 8.7, 21.0]}`

**Réponse 200 :**
```json
{
  "operation": "test_normalite_shapiro_wilk",
  "resultat": {
    "statistique": 0.981, "p_value": 0.958,
    "est_normale": true,
    "interpretation": "Distribution normale (p > 0.05)"
  }
}
```

### POST /stats/test_student
Test t de Student pour comparer les moyennes de deux groupes.

**Corps :** `{"groupe1": [12.5, 15.3], "groupe2": [9.8, 17.6]}`

**Réponse 200 :**
```json
{
  "operation": "test_t_student",
  "resultat": {
    "t_statistique": 0.1857,
    "p_value": 0.871,
    "difference_significative": false
  }
}
```

## Auteur

Etudiant B