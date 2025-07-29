import unittest
from unittest.mock import MagicMock
import requests_mock
from urllib.parse import unquote
from pyticoop.dolibarr.base import DolibarrAPI
from pyticoop.dolibarr.stockmovements import StockMovementsAPI
from pyticoop.dolibarr.query import DolibarrQueryBuilder, FilterOperator, SortOrder

class TestStockMovementsAPI(unittest.TestCase):
    """Test case for the StockMovements API"""

    def setUp(self):
        self.api_client = DolibarrAPI(base_url="https://example.com/api/index.php", api_key="fake_api_key")
        self.stockmovements_api = StockMovementsAPI(self.api_client)

    @requests_mock.Mocker()
    def test_list_movements(self, mock):
        """Test listing stock movements"""
        expected_movements = [
            {"id": 1, "fk_product": 4769, "qty": 10, "type_mouvement": 1},
            {"id": 2, "fk_product": 4769, "qty": -5, "type_mouvement": 0}
        ]
        mock.get(
            "https://example.com/api/index.php/stockmovements",
            json=expected_movements,
            status_code=200
        )
        
        query = DolibarrQueryBuilder()
        params = (
            query
            .add_filter("fk_product", FilterOperator.EQUALS, 4769)
            .sort_by("date_creation", SortOrder.DESC)
            .set_limit(100)
            .build()
        )
        response = self.stockmovements_api.list_movements(params)
        
        self.assertEqual(response, expected_movements)
        
        # Decode the URL before checking the parameters
        decoded_url = unquote(mock.last_request.url)
        self.assertIn("sqlfilters=(t.fk_product:=:4769)", decoded_url)
        self.assertIn("sortfield=date_creation", decoded_url)
        self.assertIn("sortorder=DESC", decoded_url)
        self.assertIn("limit=100", decoded_url)

    @requests_mock.Mocker()
    def test_create_movement(self, mock):
        """Test creating a stock movement"""
        movement_data = {
            "fk_product": 4769,
            "qty": 15,
            "type_mouvement": 1,
            "label": "Réception commande fournisseur"
        }
        expected_response = {
            "id": 123,
            **movement_data
        }
        mock.post(
            "https://example.com/api/index.php/stockmovements",
            json=expected_response,
            status_code=201
        )
        
        response = self.stockmovements_api.create_movement(movement_data)
        
        self.assertEqual(response, expected_response)
        self.assertEqual(mock.last_request.json(), movement_data)


if __name__ == '__main__':
    unittest.main()