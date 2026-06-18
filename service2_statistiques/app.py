# Importation des bibliothèques nécessaires
from flask import Flask, request, jsonify
import numpy as np
from scipy import stats

# Création de l'application Flask
app = Flask(__name__)

# Fonction utilitaire qui valide et convertit les données reçues en tableau numpy
def validate_data(data  , key='data'):
    """Valide et retourne une liste de nombres."""
    if key not in data:
        raise ValueError(f"Cle '{key}' manquante dans la requete")
    values = data[key]
    if not isinstance(values, list) or len(values) < 2:
        raise ValueError("'data' doit etre une liste d'au moins 2 valeurs")
    return np.array(values, dtype=float)

# Route 1 : calcul des statistiques descriptives
@app.route('/stats/describe', methods=['POST'])
def describe():
    data = request.get_json()
    try:
        values = validate_data(data)
        result = {
            'n': int(len(values)),
            'moyenne': round(float(np.mean(values)), 4),
            'mediane': round(float(np.median(values)), 4),
            'ecart_type': round(float(np.std(values, ddof=1)), 4),
            'variance': round(float(np.var(values, ddof=1)), 4),
            'minimum': round(float(np.min(values)), 4),
            'maximum': round(float(np.max(values)), 4),
            'q1': round(float(np.percentile(values, 25)), 4),
            'q3': round(float(np.percentile(values, 75)), 4),
            'etendue': round(float(np.ptp(values)), 4),
        }
        return jsonify({'operation': 'description', 'resultat': result})
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400

# Route 2 : calcul de la corrélation de Pearson entre deux séries    
@app.route('/stats/correlation', methods=['POST'])
def correlation():
    data = request.get_json()
    try:
        x = validate_data(data, 'x')
        y = validate_data(data, 'y')
        if len(x) != len(y):
            return jsonify({'erreur': 'x et y doivent avoir la meme longueur'}), 400
        r, p_value = stats.pearsonr(x, y)
        interpretation = (
            'forte' if abs(r) > 0.7
            else 'moderee' if abs(r) > 0.4
            else 'faible'
        )
        return jsonify({
            'operation': 'correlation_pearson',
            'resultat': {
            'r': round(r, 4),
            'p_value': round(p_value, 6),
            'interpretation': interpretation,
            'significatif': bool(p_value < 0.05)
            }
        })
    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400

# Lancement du serveur Flask sur le port 5002   
if __name__ == '__main__':
    app.run(debug=True, port=5002)



