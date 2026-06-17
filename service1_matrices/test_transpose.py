import requests

BASE_URL = "http://localhost:5001"

def tester_la_transposee():
    payload = {"A": [[1, 2, 3], [4, 5, 6]]}
    response = requests.post(f"{BASE_URL}/matrices/transpose", json=payload)
    
    if response.status_code == 200:
        print("Test Succes Reussi ! Reponse :", response.json()["resultat"])
    else:
        print("Echec du test Succes, code :", response.status_code)

def tester_erreur_cle_manquante():
    payload = {"MauvaiseCle": [[1, 2]]}
    response = requests.post(f"{BASE_URL}/matrices/transpose", json=payload)
    
    if response.status_code == 400:
        print("Test Erreur Reussi ! L'API a bien bloque la requete.")
    else:
        print("Echec du test Erreur, code recu :", response.status_code)

# Lancement manuel des fonctions
if __name__ == '__main__':
    tester_la_transposee()
    tester_erreur_cle_manquante()