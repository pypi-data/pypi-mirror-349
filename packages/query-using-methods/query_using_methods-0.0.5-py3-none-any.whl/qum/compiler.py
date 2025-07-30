from typing import Any, List, Union

from qum.expressions import Expression, TableField, Function, Subquery


def compile_expression(
    expr: Union[Expression, tuple, TableField, Function, Subquery],
    args: List[Any],
) -> str:
    """
    Compiles a given expression into its SQL string representation.

    This function recursively processes different types of expressions,
    including table fields, functions, subqueries, and logical/comparison
    operations, converting them into a format suitable for SQL queries.
    It also populates the `args` list with the actual values to be used
    as parameters in a parameterized query, preventing SQL injection.

    Args:
        expr (Union[Expression, tuple, TableField, Function, SubqueryExpression]):
            The expression to compile. This can be an instance of the `Expression`
            hierarchy (TableField, Function, SubqueryExpression) or a tuple
            representing an operation and its operands.
        args (List[Any]): A list that will be populated with the values
            corresponding to the placeholders in the compiled SQL string.
            This is used for parameterized queries.

    Returns:
        str: The compiled SQL string representation of the input expression.

    Raises:
        ValueError: If the input expression is invalid or contains an unknown operator.
    """
    if isinstance(expr, TableField):
        """
        If the expression is a TableField, simply return its name.
        The name represents the column in the SQL query.
        """
        return expr.name
    elif isinstance(expr, Function):
        """
        If the expression is a Function, compile its arguments recursively
        and then format the function call with its name and compiled arguments.
        If an alias is present, it's added to the function call.
        """
        compiled_args = [
            compile_expression(arg, args) if isinstance(arg, Expression) else repr(arg)
            for arg in expr.args
        ]
        if expr.alias:
            return f"{expr.name}({', '.join(compiled_args)}) AS {expr.alias}"
        return f"{expr.name}({', '.join(compiled_args)})"
    elif isinstance(expr, Subquery):
        """
        If the expression is a SubqueryExpression, recursively compile the
        underlying query (if it's a Query object) or use the raw SQL string.
        An alias for the subquery is also added if present.
        To avoid circular dependencies, the Query class is imported locally.
        """
        from qum.query import Query  # Import Query here to avoid circular dependency

        if isinstance(expr.subquery, Query):
            compiled_query, subquery_args = expr.subquery.compile()
            args.extend(subquery_args)
            alias_str = f" AS {expr.alias}" if expr.alias else ""
            if alias_str:
                return f"({compiled_query}){alias_str}"
            return f"{compiled_query}"
        elif isinstance(expr.subquery, str):
            alias_str = f" AS {expr.alias}" if expr.alias else ""
            if alias_str:
                return f"({expr.subquery}){alias_str}"
            return f"{expr.subquery}"
        else:
            raise ValueError("Invalid subquery expression")
    elif isinstance(expr, Expression):
        """
        If the expression is a generic Expression, access its underlying
        `expr` attribute, which is typically a tuple representing an operation.
        """
        expr = expr.expr

    if isinstance(expr, str):
        """
        If the expression is a string, it's returned directly. This can be
        used for raw SQL snippets (though using the Expression classes is preferred).
        """
        return expr

    if not isinstance(expr, tuple) or len(expr) == 0:
        """
        Ensure that the underlying expression is a non-empty tuple,
        which is expected for operations.
        """
        raise ValueError(f"Invalid expression: {expr}")

    op = expr[0]
    """
    The first element of the tuple represents the operator.
    """

    match op:
        case "=" | "!=" | "<" | "<=" | ">" | ">=":
            """
            Handle comparison operators. The field is compiled, and the value
            is added to the `args` list as a parameter. A placeholder ($n)
            is used in the SQL string.
            """
            field, value = expr[1], expr[2]
            args.append(value)
            if isinstance(field, Expression):
                return f"{compile_expression(field, args)} {op} ${len(args)}"
            else:
                return f"{field} {op} ${len(args)}"

        case "IS NULL" | "IS NOT NULL":
            """
            Handle IS NULL and IS NOT NULL operators. Only the field needs to be compiled.
            """
            return f"{compile_expression(expr[1], args)} {op}"

        case "LIKE" | "ILIKE" | "NOT LIKE" | "NOT ILIKE":
            """
            Handle LIKE and ILIKE operators. The field is compiled, and the pattern
            is added to the `args` list as a parameter.
            """
            field, pattern = expr[1], expr[2]
            args.append(pattern)
            return f"{compile_expression(field, args)} {op} ${len(args)}"

        case "IN" | "NOT IN":
            """
            Handle IN and NOT IN operators. If the values are a list, each value
            is added to the `args` list, and placeholders are created. If the
            values are a SubqueryExpression, it's compiled recursively.
            """
            field, values = expr[1], expr[2]
            if isinstance(values, list):
                placeholders = []
                for v in values:
                    args.append(v)
                    placeholders.append(f"${len(args)}")
                return f"{compile_expression(field, args)} {op} ({', '.join(placeholders)})"
            elif isinstance(values, Subquery):
                return f"{compile_expression(field, args)} {op} ({compile_expression(values, args)})"
            else:
                raise ValueError(f"Invalid value for {op} operator: {values}")

        case "BETWEEN":
            """
            Handle the BETWEEN operator. The field, start, and end values are compiled
            and added to the `args` list.
            """
            field, start, end = expr[1], expr[2], expr[3]
            args.append(start)
            args.append(end)
            return f"{compile_expression(field, args)} BETWEEN ${len(args)-1} AND ${len(args)}"

        case "AND" | "OR":
            """
            Handle logical AND and OR operators. Both the left and right operands
            are compiled recursively and combined with the operator in parentheses
            to ensure correct precedence.
            """
            left = compile_expression(expr[1], args)
            right = compile_expression(expr[2], args)
            return f"({left} {op} {right})"

        case "NOT":
            """
            Handle the logical NOT operator. The inner expression is compiled
            and enclosed in parentheses.
            """
            inner = compile_expression(expr[1], args)
            return f"NOT ({inner})"

        case "AS":
            field = expr[1]
            alias = expr[2]
            return f"{field} AS {alias}"

        case _:
            """
            If an unknown operator is encountered, raise a ValueError.
            """
            raise ValueError(f"Unknown operator: {op}")
