import unittest
import requests_mock
from pyticoop.dolibarr.base import DolibarrAPI
from pyticoop.dolibarr.documents import DocumentsAPI
import base64


class TestDocumentsAPI(unittest.TestCase):

    def setUp(self):
        # Initialisation du client API et de l'API des documents
        self.api_client = DolibarrAPI(
            base_url="https://example.com/api/index.php",
            api_key="fake_api_key",
        )
        self.documents_api = DocumentsAPI(self.api_client)

    @requests_mock.Mocker()
    def test_list_documents(self, mock):
        # Simuler la réponse d'une liste de documents
        mock.get(
            "https://example.com/api/index.php/documents",
            json={"data": ["doc1", "doc2"]},
            status_code=200,
        )

        # Appel de la méthode list_documents
        response = self.documents_api.list_documents(modulepart="invoice")

        # Vérification de la réponse
        self.assertEqual(response, {"data": ["doc1", "doc2"]})

    @requests_mock.Mocker()
    def test_get_document(self, mock):
        # Simuler la réponse pour la récupération d'un document spécifique
        mock.get(
            "https://example.com/api/index.php/documents",
            json={"id": 1, "ref": "DOC001"},
            status_code=200,
        )

        # Appel de la méthode get_document
        response = self.documents_api.get_document(
            modulepart="invoice", document_id=1
        )

        # Vérification de la réponse
        self.assertEqual(response, {"id": 1, "ref": "DOC001"})

    @requests_mock.Mocker()
    def test_download_document(self, mock):
        # Simuler la réponse pour le téléchargement d'un document
        mock_response = {
            "filename": "IN201701-999.pdf",
            "content-type": "application/pdf",
            "filesize": 1024,
            "content": base64.b64encode(b"file content").decode("utf-8"),
            "encoding": "base64",
        }
        mock.get(
            "https://example.com/api/index.php/documents/download",
            json=mock_response,
            status_code=200,
        )

        # Appel de la méthode download_document
        response = self.documents_api.download_document(
            module_part="invoice",
            original_file="IN201701-999/IN201701-999.pdf",
        )

        # Vérification de la réponse
        self.assertEqual(response["filename"], "IN201701-999.pdf")
        self.assertEqual(response["content-type"], "application/pdf")
        self.assertEqual(response["filesize"], 1024)
        self.assertEqual(response["encoding"], "base64")

        # Décoder le contenu base64 pour vérifier le contenu du fichier
        decoded_content = base64.b64decode(response["content"])
        self.assertEqual(decoded_content, b"file content")


if __name__ == "__main__":
    unittest.main()
