import requests  # Bibliothèque pour envoyer des requêtes HTTP

def test_describe():
    # URL de la route à tester
    url = "http://localhost:5002/stats/describe"
    # Données envoyées : tableau de 8 valeurs numériques
    payload = {"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}
    response = requests.post(url, json=payload)
    # Vérifie que le serveur répond bien avec un code 200
    assert response.status_code == 200
    result = response.json()["resultat"]
    # Vérifie que le nombre de valeurs est correct
    assert result["n"] == 8
    # Vérifie que la moyenne calculée est correcte
    assert result["moyenne"] == 13.6875
    print("Test /stats/describe OK :", result)

def test_describe_erreur():
    url = "http://localhost:5002/stats/describe"
    # Test avec une seule valeur : doit retourner une erreur 400
    response = requests.post(url, json={"data": [1]})
    assert response.status_code == 400
    print("Test erreur OK :", response.json())

if __name__ == "__main__":
    # Lancement des deux tests
    test_describe()
    test_describe_erreur()