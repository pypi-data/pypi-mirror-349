from typing import Dict, Optional, Any, List
from pyticoop.dolibarr.base import DolibarrAPI


class DocumentsAPI:
    """
    Gestion des documents via l'API Dolibarr.
    """

    def __init__(self, client: DolibarrAPI) -> None:
        self.client = client

    def list_documents(
        self, modulepart: str, filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Récupère la liste des documents.

        :param modulepart: Nom du module ou de la zone concernée ('thirdparty', 'member', 'proposal', 'order', 'invoice', 'shipment', 'project', ...)
        :param filters: Dictionnaire pour filtrer les résultats.
        :return: Liste de documents.
        """
        params = filters if filters else {}
        params["modulepart"] = modulepart
        return self.client.get("/documents", params=params)

    def get_documents(
        self,
        modulepart: str,
        document_id: Optional[int] = None,
        ref: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Récupère les détails d'un document spécifique.

        :param modulepart: Nom du module ou de la zone concernée ('thirdparty', 'member', 'proposal', 'order', 'invoice', 'shipment', 'project', ...)
        :param document_id: ID du document.
        :param ref: Référence du document.
        :return: Détails du document.
        """
        params = {"modulepart": modulepart}
        if document_id:
            params["id"] = document_id
        if ref:
            params["ref"] = ref
        return self.client.get("/documents", params=params)

    def download_document(
        self, module_part: str, original_file: str
    ) -> Dict[str, Any]:
        """
        Télécharge un document.

        :param module_part: Nom du module ou de la zone concernée par le téléchargement du fichier ('facture', ...)
        :param original_file: Chemin relatif avec le nom de fichier, relatif au modulepart (par exemple: IN201701-999/IN201701-999.pdf)
        :return: Contenu du fichier téléchargé.
        """
        params = {"module_part": module_part, "original_file": original_file}
        return self.client.get("/documents/download", params=params)
