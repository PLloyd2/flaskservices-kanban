"""
Tests unitaires — Service 4 : Chargement CSV → MySQL
======================================================
Couverture :
  - POST /upload/csv  (upload_csv)
  - GET  /upload/series (list_series)

La base de données MySQL est entièrement mockée : aucune connexion réelle
n'est nécessaire pour exécuter cette suite de tests.

Dépendances :
    pip install flask pandas mysql-connector-python python-dotenv pytest
Lancement :
    pytest test_service4.py -v
"""

import io
import json
import unittest
from unittest.mock import MagicMock, patch

import sys, os

service4_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'service4_csv_mysql'))
sys.path.insert(0, service4_path)

from app import app, TAILLE_MAX_OCTETS


# ═════════════════════════════════════════════════════════════════════════════
# Helpers
# ═════════════════════════════════════════════════════════════════════════════

def _csv_file(contenu: str, nom: str = "test.csv"):
    """Crée un objet FileStorage simulé à partir d'une chaîne CSV."""
    return (io.BytesIO(contenu.encode("utf-8")), nom)


def _post_csv(client, contenu: str, nom: str = "test.csv", cle: str = "file"):
    """Envoie une requête POST /upload/csv avec le contenu CSV fourni."""
    data = {cle: _csv_file(contenu, nom)}
    return client.post(
        "/upload/csv",
        data=data,
        content_type="multipart/form-data",
    )


# ═════════════════════════════════════════════════════════════════════════════
# Fixture CSV valide (colonnes complètes)
# ═════════════════════════════════════════════════════════════════════════════

CSV_VALIDE = """\
nom_serie,valeur,categorie,date_mesure
serie_A,12.50,temperature,2024-01-15
serie_A,15.30,temperature,2024-01-16
serie_B,45.10,pression,2024-01-15
"""

CSV_MINIMAL = """\
nom_serie,valeur
serie_A,10.0
serie_A,20.0
"""

CSV_VALEURS_MIXTES = """\
nom_serie,valeur,categorie,date_mesure
serie_A,12.50,temperature,2024-01-15
serie_A,abc,temperature,2024-01-16
serie_A,15.00,temperature,2024-01-17
"""

CSV_TOUT_INVALIDE = """\
nom_serie,valeur
serie_A,abc
serie_A,xyz
"""

CSV_SANS_NOM_SERIE = """\
valeur,categorie
12.50,temperature
"""

CSV_SANS_VALEUR = """\
nom_serie,categorie
serie_A,temperature
"""


# ═════════════════════════════════════════════════════════════════════════════
# Classe de base : configure le client de test et le mock MySQL
# ═════════════════════════════════════════════════════════════════════════════

class BaseTestCase(unittest.TestCase):
    """Configure app.testing et fournit un mock de get_connection."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        # Mock de la connexion MySQL pour tous les tests
        self.patcher = patch("app.get_connection")
        self.mock_get_conn = self.patcher.start()

        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        self.mock_get_conn.return_value = self.mock_conn

    def tearDown(self):
        self.patcher.stop()


# ═════════════════════════════════════════════════════════════════════════════
# Tests — POST /upload/csv
# ═════════════════════════════════════════════════════════════════════════════

class TestUploadCsvValidation(BaseTestCase):
    """Cas d'erreur de validation (avant insertion BDD)."""

    # ── Clé 'file' absente ──────────────────────────────────────────────────
    def test_aucun_fichier_envoye(self):
        """400 si la clé 'file' est absente du formulaire."""
        rep = self.client.post("/upload/csv", data={}, content_type="multipart/form-data")
        self.assertEqual(rep.status_code, 400)
        corps = json.loads(rep.data)
        self.assertIn("erreur", corps)
        self.assertIn("file", corps["erreur"].lower())

    # ── Nom de fichier vide ─────────────────────────────────────────────────
    def test_nom_fichier_vide(self):
        """400 si le fichier est envoyé avec un nom vide."""
        data = {"file": (io.BytesIO(b"nom_serie,valeur\nA,1\n"), "")}
        rep = self.client.post("/upload/csv", data=data, content_type="multipart/form-data")
        self.assertEqual(rep.status_code, 400)
        corps = json.loads(rep.data)
        self.assertIn("vide", corps["erreur"].lower())

    # ── Extension non .csv ──────────────────────────────────────────────────
    def test_extension_invalide_txt(self):
        """400 si le fichier a une extension .txt."""
        rep = _post_csv(self.client, CSV_VALIDE, nom="donnees.txt")
        self.assertEqual(rep.status_code, 400)
        corps = json.loads(rep.data)
        self.assertIn(".csv", corps["erreur"].lower())

    def test_extension_invalide_xlsx(self):
        """400 si le fichier a une extension .xlsx."""
        rep = _post_csv(self.client, CSV_VALIDE, nom="donnees.xlsx")
        self.assertEqual(rep.status_code, 400)

    # ── Fichier trop volumineux ─────────────────────────────────────────────
    def test_fichier_trop_grand(self):
        """413 si le fichier dépasse 5 Mo."""
        gros_contenu = b"nom_serie,valeur\n" + b"A,1\n" * (TAILLE_MAX_OCTETS // 4 + 1)
        data = {"file": (io.BytesIO(gros_contenu), "gros.csv")}
        rep = self.client.post("/upload/csv", data=data, content_type="multipart/form-data")
        self.assertEqual(rep.status_code, 413)
        corps = json.loads(rep.data)
        self.assertIn("volumineux", corps["erreur"].lower())

    # ── Colonne 'nom_serie' manquante ───────────────────────────────────────
    def test_colonne_nom_serie_manquante(self):
        """400 si la colonne obligatoire 'nom_serie' est absente."""
        rep = _post_csv(self.client, CSV_SANS_NOM_SERIE)
        self.assertEqual(rep.status_code, 400)
        corps = json.loads(rep.data)
        self.assertIn("manquantes", corps)
        self.assertIn("nom_serie", corps["manquantes"])

    # ── Colonne 'valeur' manquante ──────────────────────────────────────────
    def test_colonne_valeur_manquante(self):
        """400 si la colonne obligatoire 'valeur' est absente."""
        rep = _post_csv(self.client, CSV_SANS_VALEUR)
        self.assertEqual(rep.status_code, 400)
        corps = json.loads(rep.data)
        self.assertIn("manquantes", corps)
        self.assertIn("valeur", corps["manquantes"])

    # ── Aucune ligne valide ─────────────────────────────────────────────────
    def test_toutes_valeurs_non_numeriques(self):
        """400 si toutes les valeurs sont non numériques (df vide après nettoyage)."""
        rep = _post_csv(self.client, CSV_TOUT_INVALIDE)
        self.assertEqual(rep.status_code, 400)
        corps = json.loads(rep.data)
        self.assertIn("valide", corps["erreur"].lower())

    # ── CSV mal formé ───────────────────────────────────────────────────────
    def test_csv_mal_forme(self):
        """400 si le contenu n'est pas un CSV lisible."""
        rep = _post_csv(self.client, "\x00\x01\x02\x03binaire")
        self.assertEqual(rep.status_code, 400)

    # ── Clé formulaire incorrecte ───────────────────────────────────────────
    def test_cle_formulaire_incorrecte(self):
        """400 si le fichier est envoyé sous une clé autre que 'file'."""
        rep = _post_csv(self.client, CSV_VALIDE, cle="csv")
        self.assertEqual(rep.status_code, 400)


# ═════════════════════════════════════════════════════════════════════════════
# Tests — POST /upload/csv (succès)
# ═════════════════════════════════════════════════════════════════════════════

class TestUploadCsvSucces(BaseTestCase):
    """Cas nominaux d'insertion réussie."""

    def test_csv_valide_complet(self):
        """201 et 3 lignes insérées avec le CSV complet à 4 colonnes."""
        rep = _post_csv(self.client, CSV_VALIDE)
        self.assertEqual(rep.status_code, 201)
        corps = json.loads(rep.data)
        self.assertEqual(corps["statut"], "success")
        self.assertEqual(corps["lignes_inserees"], 3)
        self.assertEqual(corps["lignes_invalides_ignorees"], 0)
        self.assertIn("3", corps["message"])

    def test_csv_minimal_deux_colonnes(self):
        """201 et 2 lignes insérées avec un CSV ne contenant que les colonnes requises."""
        rep = _post_csv(self.client, CSV_MINIMAL)
        self.assertEqual(rep.status_code, 201)
        corps = json.loads(rep.data)
        self.assertEqual(corps["statut"], "success")
        self.assertEqual(corps["lignes_inserees"], 2)
        self.assertEqual(corps["lignes_invalides_ignorees"], 0)

    def test_lignes_invalides_ignorees(self):
        """201 : les lignes avec valeur non numérique sont ignorées mais comptées."""
        rep = _post_csv(self.client, CSV_VALEURS_MIXTES)
        self.assertEqual(rep.status_code, 201)
        corps = json.loads(rep.data)
        self.assertEqual(corps["lignes_inserees"], 2)
        self.assertEqual(corps["lignes_invalides_ignorees"], 1)

    def test_insertion_mysql_appelee(self):
        """Vérifie que cursor.execute est appelé autant de fois qu'il y a de lignes valides."""
        _post_csv(self.client, CSV_VALIDE)
        # CSV_VALIDE contient 3 lignes de données
        self.assertEqual(self.mock_cursor.execute.call_count, 3)

    def test_commit_appele_apres_insertions(self):
        """Vérifie que conn.commit() est bien appelé après les insertions."""
        _post_csv(self.client, CSV_VALIDE)
        self.mock_conn.commit.assert_called_once()

    def test_connexion_fermee_apres_succes(self):
        """Vérifie que la connexion est fermée après une insertion réussie."""
        _post_csv(self.client, CSV_VALIDE)
        self.mock_conn.close.assert_called_once()
        self.mock_cursor.close.assert_called_once()

    def test_colonnes_supplementaires_ignorees(self):
        """Les colonnes hors COLONNES_VALIDES ne provoquent pas d'erreur."""
        csv_extra = "nom_serie,valeur,categorie,date_mesure,colonne_inconnue\nA,1.0,cat,2024-01-01,extra\n"
        rep = _post_csv(self.client, csv_extra)
        self.assertEqual(rep.status_code, 201)
        corps = json.loads(rep.data)
        self.assertEqual(corps["lignes_inserees"], 1)


# ═════════════════════════════════════════════════════════════════════════════
# Tests — POST /upload/csv (erreur BDD)
# ═════════════════════════════════════════════════════════════════════════════

class TestUploadCsvErreurBDD(BaseTestCase):
    """Erreurs survenant lors de l'accès à MySQL."""

    def test_erreur_connexion_bdd(self):
        """500 si get_connection() lève une exception."""
        self.mock_get_conn.side_effect = Exception("connexion refusée")
        rep = _post_csv(self.client, CSV_VALIDE)
        self.assertEqual(rep.status_code, 500)
        corps = json.loads(rep.data)
        self.assertIn("erreur", corps)

    def test_erreur_insertion_bdd(self):
        """500 si cursor.execute() lève une exception pendant l'insertion."""
        self.mock_cursor.execute.side_effect = Exception("table introuvable")
        rep = _post_csv(self.client, CSV_VALIDE)
        self.assertEqual(rep.status_code, 500)
        corps = json.loads(rep.data)
        self.assertIn("base de données", corps["erreur"].lower())
        self.assertIn("detail", corps)


# ═════════════════════════════════════════════════════════════════════════════
# Tests — GET /upload/series
# ═════════════════════════════════════════════════════════════════════════════

class TestListSeries(BaseTestCase):
    """Tests de la route GET /upload/series."""

    def test_retourne_liste_series(self):
        """200 avec la liste des séries lorsque la BDD contient des données."""
        self.mock_cursor.fetchall.return_value = [
            ("serie_A", 10, "2024-01-15", "2024-01-24"),
            ("serie_B", 10, "2024-01-15", "2024-01-24"),
            ("serie_C", 10, "2024-01-15", "2024-01-24"),
        ]
        rep = self.client.get("/upload/series")
        self.assertEqual(rep.status_code, 200)
        corps = json.loads(rep.data)
        self.assertIn("series", corps)
        self.assertEqual(corps["total"], 3)
        self.assertEqual(len(corps["series"]), 3)

    def test_structure_chaque_serie(self):
        """Chaque élément de 'series' contient les clés attendues."""
        self.mock_cursor.fetchall.return_value = [
            ("serie_A", 5, "2024-01-15", "2024-01-19"),
        ]
        rep = self.client.get("/upload/series")
        corps = json.loads(rep.data)
        serie = corps["series"][0]
        self.assertIn("serie", serie)
        self.assertIn("n_points", serie)
        self.assertIn("debut", serie)
        self.assertIn("fin", serie)

    def test_liste_vide_si_aucune_donnee(self):
        """200 avec une liste vide si la table donnees est vide."""
        self.mock_cursor.fetchall.return_value = []
        rep = self.client.get("/upload/series")
        self.assertEqual(rep.status_code, 200)
        corps = json.loads(rep.data)
        self.assertEqual(corps["series"], [])
        self.assertEqual(corps["total"], 0)

    def test_total_correspond_a_longueur_series(self):
        """Le champ 'total' correspond toujours au nombre d'éléments dans 'series'."""
        self.mock_cursor.fetchall.return_value = [
            ("serie_A", 3, "2024-01-15", "2024-01-17"),
            ("serie_B", 2, "2024-01-15", "2024-01-16"),
        ]
        rep = self.client.get("/upload/series")
        corps = json.loads(rep.data)
        self.assertEqual(corps["total"], len(corps["series"]))

    def test_erreur_bdd_retourne_500(self):
        """500 si get_connection() lève une exception sur /upload/series."""
        self.mock_get_conn.side_effect = Exception("timeout")
        rep = self.client.get("/upload/series")
        self.assertEqual(rep.status_code, 500)
        corps = json.loads(rep.data)
        self.assertIn("erreur", corps)
        self.assertIn("detail", corps)

    def test_connexion_fermee_apres_lecture(self):
        """La connexion et le curseur sont fermés après la lecture."""
        self.mock_cursor.fetchall.return_value = []
        self.client.get("/upload/series")
        self.mock_cursor.close.assert_called_once()
        self.mock_conn.close.assert_called_once()


# ═════════════════════════════════════════════════════════════════════════════
# Point d'entrée
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    unittest.main(verbosity=2)
