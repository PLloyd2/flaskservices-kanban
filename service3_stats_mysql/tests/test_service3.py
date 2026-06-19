import requests  # Bibliothèque pour envoyer des requêtes HTTP

# URL de base du service 3
BASE_URL = "http://localhost:5003"

# ─── Tests de la route GET /db/stats/describe ───────────────────

def test_describe_serie_A():
    # Test avec la serie_A qui existe dans la BDD
    response = requests.get(f"{BASE_URL}/db/stats/describe", params={"serie": "serie_A"})
    # Vérifie que le serveur répond bien avec un code 200
    print("Status:", response.status_code)
    print("Réponse:", response.json())
    assert response.status_code == 200
    result = response.json()
    # Vérifie que la source est bien mysql
    assert result["source"] == "mysql"
    # Vérifie que les champs attendus sont présents
    assert "resultat" in result
    assert result["resultat"]["serie"] == "serie_A"
    assert "moyenne" in result["resultat"]
    assert "ecart_type" in result["resultat"]
    print("Test describe serie_A OK :", result["resultat"])

def test_describe_serie_B():
    # Test avec la serie_B qui existe dans la BDD
    response = requests.get(f"{BASE_URL}/db/stats/describe", params={"serie": "serie_B"})
    assert response.status_code == 200
    result = response.json()
    assert result["resultat"]["serie"] == "serie_B"
    print("Test describe serie_B OK :", result["resultat"])

def test_describe_serie_inexistante():
    # Test avec une série qui n'existe pas : doit retourner une erreur 404
    response = requests.get(f"{BASE_URL}/db/stats/describe", params={"serie": "serie_inexistante"})
    assert response.status_code == 404
    print("Test describe série inexistante OK :", response.json())

def test_describe_sans_parametre():
    # Test sans paramètre 'serie' : doit retourner une erreur 400
    response = requests.get(f"{BASE_URL}/db/stats/describe")
    assert response.status_code == 400
    print("Test describe sans parametre OK :", response.json())

# ─── Tests de la route GET /db/stats/correlation ────────────────

def test_correlation_A_B():
    # Test de corrélation entre serie_A et serie_B
    response = requests.get(
        f"{BASE_URL}/db/stats/correlation",
        params={"serie_x": "serie_A", "serie_y": "serie_B"}
    )
    # Vérifie que le serveur répond bien avec un code 200
    assert response.status_code == 200
    result = response.json()
    # Vérifie que la source est bien mysql
    assert result["source"] == "mysql"
    # Vérifie que les champs r et p_value sont présents
    assert "r" in result["resultat"]
    assert "p_value" in result["resultat"]
    assert "significatif" in result["resultat"]
    print("Test correlation serie_A / serie_B OK :", result["resultat"])

def test_correlation_A_C():
    # Test de corrélation entre serie_A et serie_C
    response = requests.get(
        f"{BASE_URL}/db/stats/correlation",
        params={"serie_x": "serie_A", "serie_y": "serie_C"}
    )
    assert response.status_code == 200
    result = response.json()
    assert "r" in result["resultat"]
    print("Test correlation serie_A / serie_C OK :", result["resultat"])

def test_correlation_sans_parametre():
    # Test sans paramètres : doit retourner une erreur 400
    response = requests.get(f"{BASE_URL}/db/stats/correlation")
    assert response.status_code == 400
    print("Test correlation sans parametre OK :", response.json())

def test_correlation_serie_inexistante():
    # Test avec une série inexistante : doit retourner une erreur 404
    response = requests.get(
        f"{BASE_URL}/db/stats/correlation",
        params={"serie_x": "serie_inexistante", "serie_y": "serie_A"}
    )
    assert response.status_code == 404
    print("Test correlation serie inexistante OK :", response.json())

if __name__ == "__main__":
    # Lancement de tous les tests
    print("=== Tests route /db/stats/describe ===")
    test_describe_serie_A()
    test_describe_serie_B()
    test_describe_serie_inexistante()
    test_describe_sans_parametre()

    print("\n=== Tests route /db/stats/correlation ===")
    test_correlation_A_B()
    test_correlation_A_C()
    test_correlation_sans_parametre()
    test_correlation_serie_inexistante()

    print("\nTous les tests sont passes avec succes !")