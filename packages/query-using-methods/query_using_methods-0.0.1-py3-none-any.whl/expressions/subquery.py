from typing import TYPE_CHECKING, Optional, Union
from expressions.expression import Expression

if TYPE_CHECKING:
    from query import Query


class Subquery(Expression):
    """
    Represents a subquery used within an SQL expression (e.g., in WHERE or IN clauses).

    This class extends Expression and holds a Query object or a raw SQL string
    representing the subquery.

    Attributes:
        subquery (Union[Query, str]): The Query object or the SQL string of the subquery.
        alias (Optional[str]): An optional alias for the subquery, especially useful
                               when the subquery is used in the FROM clause (though
                               this class is primarily for subqueries within expressions).
    """

    def __init__(self, subquery: Union["Query", str], alias: Optional[str] = None):
        """
        Initializes a SubqueryExpression object.

        Args:
            subquery (Union[Query, str]): The Query object or the SQL string for the subquery.
            alias (Optional[str]): An optional alias for the subquery.
        """
        super().__init__(subquery)
        self.subquery = subquery
        self.alias = alias

    def __repr__(self):
        """
        Provides a string representation of the SubqueryExpression object.

        Returns:
            str: A string representation indicating it's a SubqueryExpression
                 and showing its subquery and optional alias.
        """
        return f"SubqueryExpression('{self.subquery}', alias='{self.alias}')"
