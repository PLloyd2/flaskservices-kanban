import requests  # Bibliothèque pour envoyer des requêtes HTTP

def test_correlation():
    # URL de la route à tester
    url = "http://localhost:5002/stats/correlation"
    # Données envoyées : deux séries x et y de 5 valeurs chacune
    payload = {"x": [1, 2, 3, 4, 5], "y": [2, 4, 5, 4, 5]}
    response = requests.post(url, json=payload)
    # Vérifie que le serveur répond bien avec un code 200
    assert response.status_code == 200
    result = response.json()["resultat"]
    # Vérifie que le coefficient r et la p_value sont bien présents
    assert "r" in result
    assert "p_value" in result
    print("Test /stats/correlation OK :", result)

def test_longueurs_differentes():
    # Test avec x et y de longueurs différentes : doit retourner une erreur 400
    url = "http://localhost:5002/stats/correlation"
    response = requests.post(url, json={"x": [1, 2, 3], "y": [1, 2]})
    assert response.status_code == 400
    print("Test erreur longueurs OK :", response.json())

if __name__ == "__main__":
    # Lancement des deux tests
    test_correlation()
    test_longueurs_differentes()