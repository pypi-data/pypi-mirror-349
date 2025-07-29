from typing import TYPE_CHECKING, Any, Optional, Union
from enums.function_type import FunctionType
from expressions.function import Function
from expressions.subquery import Subquery
from expressions.table_field import TableField

if TYPE_CHECKING:
    from query import Query


class Table:
    """
    Represents a database table and provides a convenient way to refer to its fields
    and SQL functions.

    This class uses the __getattr__ method to dynamically create TableField objects
    when you try to access an attribute that doesn't exist. This allows you to
    write code like `Table().users.name` to refer to the 'name' field of the 'users' table.
    It also provides methods for calling various SQL functions.
    """

    def __getattr__(self, name: str) -> TableField:
        """
        Dynamically creates a TableField object when an attribute is accessed.

        Args:
            name (str): The name of the attribute being accessed, which is treated
                        as the name of a field in the table.

        Returns:
            TableField: A new TableField object with the given name.
        """
        return TableField(name)

    def subquery(self, query: "Query", alias: Optional[str] = None) -> Subquery:
        """
        Creates a SubqueryExpression from a Query object.

        Args:
            query (Query): The Query object representing the subquery.
            alias (Optional[str]): An optional alias for the subquery.

        Returns:
            SubqueryExpression: A new SubqueryExpression object.
        """
        return Subquery(query, alias)

    # FUNCTIONS
    def _func(
        self,
        function: Union[str, FunctionType],
        *args: Any,
        alias: Optional[str] = None,
    ) -> Function:
        """
        A private helper method to create a Function object.

        Args:
            function (Union[str, FunctionType]): The name of the SQL function or a FunctionType enum member.
            *args (Any): Variable number of arguments for the function.
            alias (Optional[str]): An optional alias for the function's result.

        Returns:
            Function: A new Function object.
        """
        func_name = function.value if isinstance(function, FunctionType) else function
        return Function(func_name, *args, alias=alias)

    def lower(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates a LOWER() function call for the given field.

        Args:
            field (TableField): The TableField object to apply the LOWER() function to.

        Returns:
            Function: A Function object representing LOWER(field).
        """
        return self._func(FunctionType.LOWER, field, alias=alias)

    def upper(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates an UPPER() function call for the given field.

        Args:
            field (TableField): The TableField object to apply the UPPER() function to.

        Returns:
            Function: A Function object representing UPPER(field).
        """
        return self._func(FunctionType.UPPER, field, alias=alias)

    def substring(
        self, field: "TableField", start: int, length: int, alias: Optional[str] = None
    ) -> Function:
        """
        Creates a SUBSTRING() function call for the given field.

        Args:
            field (TableField): The TableField object to apply the SUBSTRING() function to.
            start (int): The starting of the substring.
            length (int): The length of the substring.

        Returns:
            Function: A Function object representing SUBSTRING(field, start, length).
        """
        return self._func(FunctionType.SUBSTRING, field, start, length, alias=alias)

    def length(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates a LENGTH() function call for the given field.

        Args:
            field (TableField): The TableField object to apply the LENGTH() function to.

        Returns:
            Function: A Function object representing LENGTH(field).
        """
        return self._func(FunctionType.LENGTH, field, alias=alias)

    def concat(self, *fields: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates a CONCAT() function call to concatenate multiple fields.

        Args:
            *fields (TableField): Variable number of TableField objects to concatenate.

        Returns:
            Function: A Function object representing CONCAT(field1, field2, ...).
        """
        return self._func(FunctionType.CONCAT, *fields, alias=alias)

    def abs(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates an ABS() function call for the given numeric field.

        Args:
            field (TableField): The TableField object to apply the ABS() function to.

        Returns:
            Function: A Function object representing ABS(field).
        """
        return self._func(FunctionType.ABS, field, alias=alias)

    def round(
        self, field: "TableField", decimals: int = 0, alias: Optional[str] = None
    ) -> Function:
        """
        Creates a ROUND() function call for the given numeric field.

        Args:
            field (TableField): The TableField object to apply the ROUND() function to.
            decimals (int, optional): The number of decimal places to round to. Defaults to 0.

        Returns:
            Function: A Function object representing ROUND(field, decimals).
        """
        return self._func(FunctionType.ROUND, field, decimals, alias=alias)

    def date(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates a DATE() function call to extract the date part from a datetime field.

        Args:
            field (TableField): The TableField object to extract the date from.

        Returns:
            Function: A Function object representing DATE(field).
        """
        return self._func(FunctionType.DATE, field, alias=alias)

    def time(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates a TIME() function call to extract the time part from a datetime field.

        Args:
            field (TableField): The TableField object to extract the time from.

        Returns:
            Function: A Function object representing TIME(field).
        """
        return self._func(FunctionType.TIME, field, alias=alias)

    def count(
        self, field: Optional[str] = "*", alias: Optional[str] = None
    ) -> Function:
        """
        Creates a COUNT() aggregate function call.

        Args:
            field (Optional[str], optional): The field to count. Defaults to "*",
                                             which counts all rows.
            alias (Optional[str], optional): An optional alias for the count result. Defaults to None.

        Returns:
            Function: A Function object representing COUNT(field) AS alias.
        """
        return self._func(FunctionType.COUNT, field, alias=alias)

    def sum(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates a SUM() aggregate function call for the given numeric field.

        Args:
            field (TableField): The TableField object to sum.
            alias (Optional[str], optional): An optional alias for the sum result. Defaults to None.

        Returns:
            Function: A Function object representing SUM(field) AS alias.
        """
        return self._func(FunctionType.SUM, field, alias=alias)

    def avg(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates an AVG() aggregate function call for the given numeric field.

        Args:
            field (TableField): The TableField object to calculate the average of.
            alias (Optional[str], optional): An optional alias for the average result. Defaults to None.

        Returns:
            Function: A Function object representing AVG(field) AS alias.
        """
        return self._func(FunctionType.AVG, field, alias=alias)

    def min(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates a MIN() aggregate function call for the given field.

        Args:
            field (TableField): The TableField object to find the minimum value of.
            alias (Optional[str], optional): An optional alias for the minimum result. Defaults to None.

        Returns:
            Function: A Function object representing MIN(field) AS alias.
        """
        return self._func(FunctionType.MIN, field, alias=alias)

    def max(self, field: "TableField", alias: Optional[str] = None) -> Function:
        """
        Creates a MAX() aggregate function call for the given field.

        Args:
            field (TableField): The TableField object to find the maximum value of.
            alias (Optional[str], optional): An optional alias for the maximum result. Defaults to None.

        Returns:
            Function: A Function object representing MAX(field) AS alias.
        """
        return self._func(FunctionType.MAX, field, alias=alias)
