import urllib.request
import json

def test_multiplication():
    url = "http://localhost:5001/matrices/multiply"
    
    # Données de test : Matrice A (2x3) et Matrice B (3x2)
    payload = {
        "A": [[1, 2, 3], [4, 5, 6]],
        "B": [[7, 8], [9, 10], [11, 12]]
    }
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            json_res = json.loads(res_body)
            
            print("Test réussi !")
            print("Réponse du serveur :", json_res)
            
            # Vérification basique du résultat attendu
            # [[1*7 + 2*9 + 3*11, ...]] -> [[58, 64], [139, 154]]
            assert json_res['resultat'] == [[58.0, 64.0], [139.0, 154.0]]
            print("Assertion OK : Le calcul est correct.")
            
    except Exception as e:
        print(f"Le test a échoué : {e}")

if __name__ == "__main__":
    test_multiplication()