import urllib.request
import json

def test_addition():
    # URL de la route addition sur le port 5001
    url = "http://localhost:5001/matrices/add"
    
    # Données de test : deux matrices 2x2 de mêmes dimensions
    payload = {
        "A": [[1, 2], [3, 4]],
        "B": [[5, 6], [7, 8]]
    }
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            json_res = json.loads(res_body)
            
            print("Test d'addition réussi !")
            print("Réponse du serveur :", json_res)
            
            # Vérification du résultat attendu : [[6.0, 8.0], [10.0, 12.0]]
            assert json_res['resultat'] == [[6.0, 8.0], [10.0, 12.0]]
            print("Assertion OK : L'addition est correcte.")
            
    except Exception as e:
        print(f"Le test a échoué : {e}")

if __name__ == "__main__":
    test_addition()