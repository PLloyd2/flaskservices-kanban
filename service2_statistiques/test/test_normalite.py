import requests  # Bibliothèque pour envoyer des requêtes HTTP

def test_normalite():
    # URL de la route à tester
    url = "http://localhost:5002/stats/test_normalite"
    # Données envoyées : tableau de 8 valeurs numériques
    payload = {"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}
    response = requests.post(url, json=payload)
    # Vérifie que le serveur répond bien avec un code 200
    assert response.status_code == 200
    result = response.json()["resultat"]
    # Vérifie que les champs est_normale et p_value sont bien présents
    assert "est_normale" in result
    assert "p_value" in result
    print("Test /stats/test_normalite OK :", result)

def test_trop_peu_valeurs():
    # Test avec une seule valeur : doit retourner une erreur 400
    url = "http://localhost:5002/stats/test_normalite"
    response = requests.post(url, json={"data": [1]})
    assert response.status_code == 400
    print("Test erreur < 2 valeurs OK :", response.json())

if __name__ == "__main__":
    # Lancement des deux tests
    test_normalite()
    test_trop_peu_valeurs()