from typing import Any, Optional
from expressions.expression import Expression


class Function(Expression):
    """
    Represents an SQL function call.

    This class extends Expression and is used to represent various SQL functions
    like aggregate functions (COUNT, SUM, AVG, MIN, MAX) and other scalar functions
    (LOWER, UPPER, etc.).

    Attributes:
        name (str): The name of the SQL function.
        args (tuple): A tuple of arguments passed to the function. These can be
                      TableField objects, literal values, or other expressions.
        alias (Optional[str]): An optional alias for the result of the function,
                               which can be used in the SELECT clause.
    """

    def __init__(self, name: str, *args: Any, alias: Optional[str] = None):
        """
        Initializes a Function object.

        Args:
            name (str): The name of the SQL function.
            *args (Any): Variable number of arguments for the function.
            alias (Optional[str]): An optional alias for the function's result.
        """
        super().__init__(name)
        self.name = name
        self.args = args
        self.alias = alias

    def __repr__(self):
        """
        Provides a string representation of the Function object.

        Returns:
            str: A string representation indicating it's a Function
                 and showing its name, arguments, and optional alias.
        """
        args_str = ", ".join(map(repr, self.args))
        alias_str = f", alias={self.alias!r}" if self.alias else ""
        return f"Function('{self.name}', {args_str}{alias_str})"
