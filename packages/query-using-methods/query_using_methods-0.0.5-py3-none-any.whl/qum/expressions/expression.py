from typing import Any


class Expression:
    """
    Represents a generic SQL expression.

    This is the base class for building more specific SQL expressions
    used in query construction. It allows for logical operations
    like AND, OR, and NOT to combine different expressions.

    Attributes:
        expr (Any): The underlying SQL expression or its components.
    """

    def __init__(self, expr: Any):
        """
        Initializes an Expression object.

        Args:
            expr (Any): The SQL expression to be represented. This can be
                        a string, a tuple representing an operator and operands,
                        or any other data structure that defines a part of an SQL query.
        """
        self.expr = expr

    def __and__(self, other: "Expression") -> "Expression":
        """
        Overloads the 'and' operator (&) to combine two expressions with 'AND'.

        Args:
            other (Expression): The other Expression object to combine with.

        Returns:
            Expression: A new Expression object representing the logical AND
                        of the current and the other expression.
        """
        return Expression(("AND", self.expr, other.expr))

    def __or__(self, other: "Expression") -> "Expression":
        """
        Overloads the 'or' operator (|) to combine two expressions with 'OR'.

        Args:
            other (Expression): The other Expression object to combine with.

        Returns:
            Expression: A new Expression object representing the logical OR
                        of the current and the other expression.
        """
        return Expression(("OR", self.expr, other.expr))

    def __invert__(self) -> "Expression":
        """
        Overloads the 'not' operator (~) to negate the current expression with 'NOT'.

        Returns:
            Expression: A new Expression object representing the negation
                        of the current expression.
        """
        return Expression(("NOT", self.expr))

    def __repr__(self):
        """
        Provides a string representation of the Expression object.

        Returns:
            str: A string representation indicating it's an Expression
                 and showing its underlying expression.
        """
        return f"Expression({self.expr})"
