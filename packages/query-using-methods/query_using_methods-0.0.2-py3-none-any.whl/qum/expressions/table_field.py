from typing import Any, List, Union
from expressions.expression import Expression
from expressions.subquery import Subquery


class TableField(Expression):
    """
    Represents a field (column) in a database table.

    This class extends Expression and provides methods for comparison
    operators, null checks, LIKE operators, IN operator, and BETWEEN operator
    that are commonly used with table fields in SQL queries.

    Attributes:
        name (str): The name of the table field (column).
    """

    def __init__(self, name: str):
        """
        Initializes a TableField object.

        Args:
            name (str): The name of the table field.
        """
        super().__init__(name)
        self.name = name

    # Comparison operators
    def __eq__(self, other: Any) -> Expression:
        """
        Overloads the equality operator (==) for comparing the field with a value.

        Args:
            other (Any): The value to compare the field with.

        Returns:
            Expression: An Expression object representing the equality comparison
                        (e.g., "column_name = value").
        """
        return Expression(("=", self.name, other))

    def __ne__(self, other: Any) -> Expression:
        """
        Overloads the inequality operator (!=) for comparing the field with a value.

        Args:
            other (Any): The value to compare the field with.

        Returns:
            Expression: An Expression object representing the inequality comparison
                        (e.g., "column_name != value").
        """
        return Expression(("!=", self.name, other))

    def __lt__(self, other: Any) -> Expression:
        """
        Overloads the less than operator (<) for comparing the field with a value.

        Args:
            other (Any): The value to compare the field with.

        Returns:
            Expression: An Expression object representing the less than comparison
                        (e.g., "column_name < value").
        """
        return Expression(("<", self.name, other))

    def __le__(self, other: Any) -> Expression:
        """
        Overloads the less than or equal to operator (<=) for comparing the field with a value.

        Args:
            other (Any): The value to compare the field with.

        Returns:
            Expression: An Expression object representing the less than or equal to comparison
                        (e.g., "column_name <= value").
        """
        return Expression(("<=", self.name, other))

    def __gt__(self, other: Any) -> Expression:
        """
        Overloads the greater than operator (>) for comparing the field with a value.

        Args:
            other (Any): The value to compare the field with.

        Returns:
            Expression: An Expression object representing the greater than comparison
                        (e.g., "column_name > value").
        """
        return Expression((">", self.name, other))

    def __ge__(self, other: Any) -> Expression:
        """
        Overloads the greater than or equal to operator (>=) for comparing the field with a value.

        Args:
            other (Any): The value to compare the field with.

        Returns:
            Expression: An Expression object representing the greater than or equal to comparison
                        (e.g., "column_name >= value").
        """
        return Expression((">=", self.name, other))

    # Null checks
    def is_null(self) -> Expression:
        """
        Creates an expression to check if the field is NULL.

        Returns:
            Expression: An Expression object representing the "IS NULL" condition
                        (e.g., "column_name IS NULL").
        """
        return Expression(("IS NULL", self.name))

    def is_not_null(self) -> Expression:
        """
        Creates an expression to check if the field is NOT NULL.

        Returns:
            Expression: An Expression object representing the "IS NOT NULL" condition
                        (e.g., "column_name IS NOT NULL").
        """
        return Expression(("IS NOT NULL", self.name))

    # LIKE operators
    def like(self, pattern: str) -> Expression:
        """
        Creates an expression for the "LIKE" operator.

        Args:
            pattern (str): The pattern to match against (e.g., 'value%').

        Returns:
            Expression: An Expression object representing the "LIKE" condition
                        (e.g., "column_name LIKE 'value%'").
        """
        return Expression(("LIKE", self.name, pattern))

    def not_like(self, pattern: str) -> Expression:
        """
        Creates an expression for the "NOT LIKE" operator.

        Args:
            pattern (str): The pattern that should not be matched (e.g., 'value%').

        Returns:
            Expression: An Expression object representing the "NOT LIKE" condition
                        (e.g., "column_name NOT LIKE 'value%'").
        """
        return Expression(("NOT LIKE", self.name, pattern))

    def ilike(self, pattern: str) -> Expression:
        """
        Creates an expression for the case-insensitive "ILIKE" operator.

        Args:
            pattern (str): The case-insensitive pattern to match against (e.g., 'Value%').

        Returns:
            Expression: An Expression object representing the "ILIKE" condition
                        (e.g., "column_name ILIKE 'Value%'").
        """
        return Expression(("ILIKE", self.name, pattern))

    def not_ilike(self, pattern: str) -> Expression:
        """
        Creates an expression for the case-insensitive "NOT ILIKE" operator.

        Args:
            pattern (str): The case-insensitive pattern that should not be matched (e.g., 'Value%').

        Returns:
            Expression: An Expression object representing the "NOT ILIKE" condition
                        (e.g., "column_name NOT ILIKE 'Value%'").
        """
        return Expression(("NOT ILIKE", self.name, pattern))

    # IN operator
    def in_(self, values: Union[List[Any], Subquery]) -> Expression:
        """
        Creates an expression for the "IN" operator.

        Args:
            values (Union[List[Any], SubqueryExpression]): A list of values or a subquery
                                                           to check if the field's value is in.

        Returns:
            Expression: An Expression object representing the "IN" condition
                        (e.g., "column_name IN (value1, value2)" or
                        "column_name IN (SELECT ...)").
        """
        return Expression(("IN", self.name, values))

    def not_in(self, values: Union[List[Any], Subquery]) -> Expression:
        """
        Creates an expression for the "NOT IN" operator.

        Args:
            values (Union[List[Any], SubqueryExpression]): A list of values or a subquery
                                                           to check if the field's value is not in.

        Returns:
            Expression: An Expression object representing the "NOT IN" condition
                        (e.g., "column_name NOT IN (value1, value2)" or
                        "column_name NOT IN (SELECT ...)").
        """
        return Expression(("NOT IN", self.name, values))

    # BETWEEN operator
    def between(self, start: Any, end: Any) -> Expression:
        """
        Creates an expression for the "BETWEEN" operator.

        Args:
            start (Any): The starting value of the range.
            end (Any): The ending value of the range.

        Returns:
            Expression: An Expression object representing the "BETWEEN" condition
                        (e.g., "column_name BETWEEN start_value AND end_value").
        """
        return Expression(("BETWEEN", self.name, start, end))

    def as_(self, alias: str) -> Expression:
        return Expression(("AS", self.name, alias))

    def __repr__(self):
        """
        Provides a string representation of the TableField object.

        Returns:
            str: A string representation indicating it's a TableField
                 and showing its name and optional alias.
        """
        return f"TableField('{self.name}')"
