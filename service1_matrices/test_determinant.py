import requests

# L'adresse de base de ton service Flask (port 5001)
BASE_URL = "http://localhost:5001"

def tester_le_determinant():
    # On prepare une matrice carree (2x2) dont le determinant vaut (1*4) - (2*3) = -2
    payload = {"A": [[1, 2], [3, 4]]}
    
    # On envoie la requete POST vers la route du determinant
    response = requests.post(f"{BASE_URL}/matrices/determinant", json=payload)
    
    # Si le serveur repond 200 (OK), le calcul a reussi
    if response.status_code == 200:
        print("Test Succes Reussi ! Reponse :", response.json()["resultat"])
    else:
        print("Echec du test Succes, code :", response.status_code)

def tester_erreur_matrice_non_carree():
    # On envoie expres une matrice non carree (2x3) pour declencher l'erreur 400
    payload = {"A": [[1, 2, 3], [4, 5, 6]]}
    
    # On envoie la requete au serveur
    response = requests.post(f"{BASE_URL}/matrices/determinant", json=payload)
    
    # Si le serveur repond 400 (Bad Request), cela veut dire qu'il a bien bloque le calcul
    if response.status_code == 400:
        print("Test Erreur Reussi ! L'API a bien bloque la matrice non carree.")
    else:
        print("Echec du test Erreur, code recu :", response.status_code)

# Lancement manuel des fonctions de test
if __name__ == '__main__':
    tester_le_determinant()
    tester_erreur_matrice_non_carree()