import requests  # Bibliothèque pour envoyer des requêtes HTTP

def test_student():
    # URL de la route à tester
    url = "http://localhost:5002/stats/test_student"
    # Données envoyées : deux groupes de valeurs numériques à comparer
    payload = {
        "groupe1": [12.5, 15.3, 8.7, 21.0],
        "groupe2": [9.8, 17.6, 11.4, 13.2]
    }
    response = requests.post(url, json=payload)
    # Vérifie que le serveur répond bien avec un code 200
    assert response.status_code == 200
    result = response.json()["resultat"]
    # Vérifie que les champs t_statistique et p_value sont bien présents
    assert "t_statistique" in result
    assert "p_value" in result
    # Vérifie que le champ difference_significative est un booléen
    assert isinstance(result["difference_significative"], bool)
    print("Test /stats/test_student OK :", result)

def test_groupe_manquant():
    # Test sans le groupe2 : doit retourner une erreur 400
    url = "http://localhost:5002/stats/test_student"
    response = requests.post(url, json={"groupe1": [1, 2, 3]})
    assert response.status_code == 400
    print("Test erreur groupe manquant OK :", response.json())

if __name__ == "__main__":
    # Lancement des deux tests
    test_student()
    test_groupe_manquant()