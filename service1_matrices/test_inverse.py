import requests

# L'adresse de base de ton service Flask (port 5001)
BASE_URL = "http://localhost:5001"

def tester_l_inverse():
    # On prepare une matrice carree inversible (2x2)
    payload = {"A": [[4, 7], [2, 6]]}
    
    # On envoie la requete POST vers la route de l'inverse
    response = requests.post(f"{BASE_URL}/matrices/inverse", json=payload)
    
    # Si le serveur repond 200 (OK), le calcul a reussi
    if response.status_code == 200:
        print("Test Succes Reussi ! Reponse :", response.json()["resultat"])
    else:
        print("Echec du test Succes, code :", response.status_code)

def tester_erreur_matrice_singuliere():
    # On envoie une matrice dont le determinant est égal à 0 (non inversible)
    payload = {"A": [[1, 2], [2, 4]]}
    
    # On envoie la requete au serveur
    response = requests.post(f"{BASE_URL}/matrices/inverse", json=payload)
    
    # Si le serveur repond 400 (Bad Request), il a bien bloque le calcul de la matrice singuliere
    if response.status_code == 400:
        print("Test Erreur Reussi ! L'API a bien bloque la matrice singuliere.")
    else:
        print("Echec du test Erreur, code recu :", response.status_code)

# Lancement manuel des fonctions de test
if __name__ == '__main__':
    tester_l_inverse()
    tester_erreur_matrice_singuliere()