from datetime import date, datetime
from typing import Union, List, Optional
from enum import Enum


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


class FilterOperator(Enum):
    EQUALS = ":=:"
    NOT_EQUALS = "<>:"
    GREATER_THAN = ":>:"
    LESS_THAN = ":<:"
    GREATER_EQUAL = ":>=:"
    LESS_EQUAL = ":<=:"
    LIKE = " LIKE:"  # Space is important


class DolibarrQueryBuilder:
    """
    Helper class to build Dolibarr API queries with proper formatting
    """

    def __init__(self):
        self._filters: List[str] = []
        self._sort_field: Optional[str] = None
        self._sort_order: Optional[SortOrder] = None
        self._limit: Optional[int] = None
        self._page: Optional[int] = None

    def add_filter(
        self,
        field: str,
        operator: FilterOperator,
        value: Union[str, int, float, date, datetime],
    ) -> "DolibarrQueryBuilder":
        """
        Add a filter condition

        Example:
            builder.add_filter("t.fk_product", FilterOperator.EQUALS, 4769)
        """
        if isinstance(value, (date, datetime)):
            formatted_value = value.strftime("%Y-%m-%d")
            self._filters.append(
                f"(t.{field}{operator.value}'{formatted_value}')"
            )
        else:
            self._filters.append(f"(t.{field}{operator.value}{value})")
        return self

    def sort_by(
        self, field: str, order: SortOrder = SortOrder.ASC
    ) -> "DolibarrQueryBuilder":
        """
        Set the sort field and order

        Example:
            builder.sort_by("date_creation", SortOrder.DESC)
        """
        self._sort_field = field
        self._sort_order = order
        return self

    def set_limit(self, limit: int) -> "DolibarrQueryBuilder":
        """Set the maximum number of records to return"""
        self._limit = limit
        return self

    def set_page(self, page: int) -> "DolibarrQueryBuilder":
        """Set the page number for pagination"""
        self._page = page
        return self

    def build(self) -> dict:
        """
        Build the final query parameters dictionary

        Returns:
            Dict containing all the query parameters
        """
        params = {}

        if self._filters:
            params["sqlfilters"] = " AND ".join(self._filters)

        if self._sort_field:
            params["sortfield"] = self._sort_field
            params["sortorder"] = self._sort_order.value

        if self._limit is not None:
            params["limit"] = self._limit

        if self._page is not None:
            params["page"] = self._page

        return params


# Example usage:
"""
# Create a new query builder
query = DolibarrQueryBuilder()

# Build a query for products created after January 1st, 2024
# with a specific product ID, sorted by creation date
params = (
    query
    .add_filter("fk_product", FilterOperator.EQUALS, 4769)
    .add_filter("date_creation", FilterOperator.GREATER_THAN, date(2024, 1, 1))
    .sort_by("date_creation", SortOrder.DESC)
    .set_limit(100)
    .set_page(0)
    .build()
)

# Use with the API
movements = stock_movements_api.list_movements(filters=params)
"""
