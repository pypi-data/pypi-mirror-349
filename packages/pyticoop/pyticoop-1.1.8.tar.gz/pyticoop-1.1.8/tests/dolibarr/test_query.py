import unittest
from datetime import date, datetime
from pyticoop.dolibarr.query import DolibarrQueryBuilder, FilterOperator, SortOrder

class TestDolibarrQueryBuilder(unittest.TestCase):
    """Test case for the DolibarrQueryBuilder"""

    def setUp(self):
        self.query_builder = DolibarrQueryBuilder()

    def test_single_filter(self):
        """Test adding a single filter condition"""
        params = (
            self.query_builder
            .add_filter("fk_product", FilterOperator.EQUALS, 4769)
            .build()
        )
        
        self.assertEqual(params["sqlfilters"], "(t.fk_product:=:4769)")

    def test_multiple_filters(self):
        """Test adding multiple filter conditions"""
        params = (
            self.query_builder
            .add_filter("fk_product", FilterOperator.EQUALS, 4769)
            .add_filter("type_mouvement", FilterOperator.EQUALS, 1)
            .build()
        )
        
        self.assertEqual(
            params["sqlfilters"],
            "(t.fk_product:=:4769) AND (t.type_mouvement:=:1)"
        )

    def test_date_filter(self):
        """Test filtering with date values"""
        test_date = date(2024, 1, 15)
        params = (
            self.query_builder
            .add_filter("date_creation", FilterOperator.GREATER_THAN, test_date)
            .build()
        )
        
        self.assertEqual(
            params["sqlfilters"],
            "(t.date_creation:>:'2024-01-15')"
        )

    def test_datetime_filter(self):
        """Test filtering with datetime values"""
        test_datetime = datetime(2024, 1, 15, 10, 30, 0)
        params = (
            self.query_builder
            .add_filter("date_creation", FilterOperator.GREATER_THAN, test_datetime)
            .build()
        )
        
        self.assertEqual(
            params["sqlfilters"],
            "(t.date_creation:>:'2024-01-15')"
        )

    def test_sort_by(self):
        """Test setting sort parameters"""
        params = (
            self.query_builder
            .sort_by("date_creation", SortOrder.DESC)
            .build()
        )
        
        self.assertEqual(params["sortfield"], "date_creation")
        self.assertEqual(params["sortorder"], "DESC")

    def test_pagination(self):
        """Test setting pagination parameters"""
        params = (
            self.query_builder
            .set_limit(100)
            .set_page(2)
            .build()
        )
        
        self.assertEqual(params["limit"], 100)
        self.assertEqual(params["page"], 2)

    def test_complex_query(self):
        """Test building a complex query with multiple parameters"""
        test_date = date(2024, 1, 1)
        params = (
            self.query_builder
            .add_filter("fk_product", FilterOperator.EQUALS, 4769)
            .add_filter("date_creation", FilterOperator.GREATER_EQUAL, test_date)
            .add_filter("type_mouvement", FilterOperator.EQUALS, 1)
            .sort_by("date_creation", SortOrder.DESC)
            .set_limit(100)
            .set_page(0)
            .build()
        )
        
        expected_filters = (
            "(t.fk_product:=:4769) AND "
            "(t.date_creation:>=:'2024-01-01') AND "
            "(t.type_mouvement:=:1)"
        )
        
        self.assertEqual(params["sqlfilters"], expected_filters)
        self.assertEqual(params["sortfield"], "date_creation")
        self.assertEqual(params["sortorder"], "DESC")
        self.assertEqual(params["limit"], 100)
        self.assertEqual(params["page"], 0)

    def test_like_operator(self):
        """Test using the LIKE operator for text search"""
        params = (
            self.query_builder
            .add_filter("label", FilterOperator.LIKE, "test%")
            .build()
        )
        
        self.assertEqual(params["sqlfilters"], "(t.label LIKE:test%)")

    def test_empty_query(self):
        """Test building a query with no parameters set"""
        params = self.query_builder.build()
        
        self.assertEqual(params, {})

    def test_chain_independence(self):
        """Test that each chain creates independent parameters"""
        first_query = (
            self.query_builder
            .add_filter("fk_product", FilterOperator.EQUALS, 4769)
            .build()
        )
        
        # Create a new query without clearing the first one
        second_query = (
            DolibarrQueryBuilder()
            .add_filter("type_mouvement", FilterOperator.EQUALS, 1)
            .build()
        )
        
        self.assertEqual(first_query["sqlfilters"], "(t.fk_product:=:4769)")
        self.assertEqual(second_query["sqlfilters"], "(t.type_mouvement:=:1)")


if __name__ == '__main__':
    unittest.main()