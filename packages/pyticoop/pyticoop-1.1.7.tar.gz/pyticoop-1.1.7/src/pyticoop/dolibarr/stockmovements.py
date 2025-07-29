from pyticoop.dolibarr.base import DolibarrAPI
from pyticoop.dolibarr.query import DolibarrQueryBuilder
from typing import Optional, Union, Dict


class StockMovementsAPI:
    """
    Gestion des mouvements de stock via l'API Dolibarr.

    Examples:
        >>> # Create a movement for a specific product
        >>> api = StockMovementsAPI(client)
        >>>
        >>> # List movements with filters
        >>> query = DolibarrQueryBuilder()
        >>> params = (
        ...     query
        ...     .add_filter("fk_product", FilterOperator.EQUALS, 4769)
        ...     .sort_by("date_creation", SortOrder.DESC)
        ...     .set_limit(100)
        ...     .build()
        ... )
        >>> movements = api.list_movements(filters=params)
    """

    def __init__(self, client: DolibarrAPI):
        self.client = client

    def list_movements(
        self, filters: Optional[Union[Dict, DolibarrQueryBuilder]] = None
    ):
        """
        Récupère la liste des mouvements de stock.

        Args:
            filters: Dictionnaire de filtres ou instance de DolibarrQueryBuilder.
                    Utilisez DolibarrQueryBuilder pour une construction facilitée des requêtes.

        Paramètres disponibles:
            - sortfield: Champ de tri
            - sortorder: Ordre de tri (ASC ou DESC)
            - limit: Nombre maximum de résultats
            - page: Numéro de page
            - sqlfilters: Filtres SQL au format Dolibarr

        Examples:
            >>> # Utilisation simple
            >>> movements = api.list_movements({"limit": 100})
            >>>
            >>> # Utilisation avec QueryBuilder
            >>> query = DolibarrQueryBuilder()
            >>> params = query.add_filter("fk_product", FilterOperator.EQUALS, 4769).build()
            >>> movements = api.list_movements(params)

        Returns:
            Liste des mouvements de stock.
        """
        if isinstance(filters, DolibarrQueryBuilder):
            filters = filters.build()
        return self.client.get("/stockmovements", params=filters)

    def create_movement(self, movement_data: dict):
        """
        Crée un nouveau mouvement de stock.

        Args:
            movement_data: Dictionnaire contenant les informations du mouvement de stock.

        Returns:
            Mouvement de stock créé.
        """
        return self.client.post("/stockmovements", json=movement_data)
