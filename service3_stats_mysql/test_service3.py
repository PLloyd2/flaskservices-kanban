import requests

BASE = "http://localhost:5003"

def test_describe_ok():
    r = requests.get(f"{BASE}/db/stats/describe", params={"serie": "serie_A"})
    assert r.status_code == 200
    data = r.json()
    assert data["source"] == "mysql"
    assert data["resultat"]["n"] > 0
    assert "moyenne" in data["resultat"]
    print("test_describe_ok passé")

def test_describe_serie_inexistante():
    r = requests.get(f"{BASE}/db/stats/describe", params={"serie": "inexistant"})
    assert r.status_code == 404
    print("test_describe_serie_inexistante passé")

def test_describe_sans_parametre():
    r = requests.get(f"{BASE}/db/stats/describe")
    assert r.status_code == 400
    print("test_describe_sans_parametre passé")

def test_correlation_ok():
    r = requests.get(f"{BASE}/db/stats/correlation", params={"serie_x": "serie_A", "serie_y": "serie_B"})
    assert r.status_code == 200
    data = r.json()
    assert data["source"] == "mysql"
    assert "r" in data["resultat"]
    assert "p_value" in data["resultat"]
    print("test_correlation_ok passé")

def test_correlation_sans_parametre():
    r = requests.get(f"{BASE}/db/stats/correlation")
    assert r.status_code == 400
    print("test_correlation_sans_parametre passé")

def test_correlation_serie_inexistante():
    r = requests.get(f"{BASE}/db/stats/correlation", params={"serie_x": "inexistant", "serie_y": "serie_B"})
    assert r.status_code == 404
    print("test_correlation_serie_inexistante passé")

if __name__ == "__main__":
    print("Lancement des tests du Service 3...\n")
    test_describe_ok()
    test_describe_serie_inexistante()
    test_describe_sans_parametre()
    test_correlation_ok()
    test_correlation_sans_parametre()
    test_correlation_serie_inexistante()
    print("\nTous les tests sont passés !")