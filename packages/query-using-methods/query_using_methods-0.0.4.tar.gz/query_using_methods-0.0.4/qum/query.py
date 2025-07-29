import datetime
import math
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from asyncpg import PostgresError
import pytz
from loguru._logger import Logger


from qum.compiler import compile_expression
from qum.database import Database
from qum.enums.order_type import OrderType
from qum.expressions import (
    Expression,
    Function,
    Table,
    TableField,
)

T = TypeVar("T")


class Query(Generic[T]):
    def __init__(self, table_name: str, model: Type[T], db: Database, logger: Logger):
        if not isinstance(table_name, str) or not table_name.strip():
            raise ValueError("`table_name` must be a non-empty string")
        if not isinstance(db, Database):
            raise TypeError("`db` must be an instance of the Database class")
        if logger is not None and not isinstance(logger, Logger):
            raise TypeError("`logger` must be an instance of Logger")

        self.table_name = table_name
        self.model = model
        self.db = db
        self.logger = logger
        self._select_fields: List[Union[TableField, Function]] = []
        self._where_clause: Optional[Expression] = None
        self._order_by_clause: Optional[str] = None
        self._limit_clause: Optional[int] = None
        self._offset_clause: Optional[int] = None
        self._distinct: bool = False
        self._distinct_on: Optional[TableField] = None
        self._group_by_fields: List[TableField] = []
        self._query_args: List[Any] = []

    def select(
        self,
        fields_lambda: Callable[
            [T],
            Union[
                TableField,
                Function,
                str,
                Expression,
                List[TableField],
                List[str],
                List[Function],
                List[Expression],
            ],
        ],
    ) -> "Query[T]":
        """
        Specifies the columns to be selected for the query.

        This method allows you to define which columns will be included in the
        results of your database query. The `fields_lambda` argument should be a
        callable that accepts a single argument (representing the table object)
        and returns a `TableField`, `Function`, a string representing a column name,
        or a list containing any combination of these.

        Use Cases:
        1. Selecting a single column using a TableField object:
           ```python
           query.select(lambda t: t.name)
           ```

        2. Selecting a single column using a string:
           ```python
           query.select(lambda t: "email")
           ```

        3. Selecting a function with a alias:
           ```python
           query.select(lambda t: Table().count(field=t.id, alias="total"))
           ```

        4. Selecting multiple columns as a list of TableField objects:
           ```python
           query.select(lambda t: [t.first_name, t.last_name])
           ```

        5. Selecting multiple columns as a list of strings:
           ```python
           query.select(lambda t: ["product_id", "price"])
           ```

        6. Selecting a mix of TableField and string columns:
           ```python
           query.select(lambda t: [t.created_at, "updated_at"])
           ```

        7. Selecting a column with a specific alias using `as_()` on a TableField:
           ```python
           query.select(lambda t: t.user_id.as_("identifier"))
           ```

        8. Selecting multiple functions:
           ```python
           query.select(lambda t: [Table().avg(field=t.rating, alias="avg_rating"), Table().min(field=t.rating, alias="min_rating")])
           ```

        9. Selecting a substring of a column:
            ```python
            query.select(lambda t: Table().substring(field=t.description, start=1, length=50, alias="short_desc"))
            ```

        10. Selecting the length of a string column:
            ```python
            query.select(lambda t: Table().length(field=t.username, alias="username_length"))
            ```

        Each subsequent call to the `select` method will clear the previously
        selected fields and set the new ones.
        """
        self.logger.debug("Entering select method.")
        self._select_fields = []  # Clear previous fields on each select call
        try:
            if not callable(fields_lambda):
                raise TypeError("fields_lambda must be a callable")

            table = Table()
            fields = fields_lambda(table)

            if fields is None:
                raise ValueError("select lambda cannot return None")

            if isinstance(fields, list):
                if not fields:
                    raise ValueError("select lambda returned an empty list")
                for field in fields:
                    if isinstance(field, str):
                        self._select_fields.append(TableField(field.strip()))
                    elif isinstance(field, (TableField, Function)):
                        self._select_fields.append(field)
                    elif isinstance(field, Expression):
                        self._select_fields.append(
                            TableField(compile_expression(field, self._query_args))
                        )
                    else:
                        raise TypeError(
                            f"Elements in select list must be str, TableField, or Function, not {type(field).__name__}"
                        )
            elif isinstance(fields, str):
                self._select_fields.append(TableField(fields.strip()))
            elif isinstance(fields, (TableField, Function)):
                self._select_fields.append(fields)
            elif isinstance(fields, Expression):
                self._select_fields.append(
                    TableField(compile_expression(fields, self._query_args))
                )
            else:
                raise TypeError(
                    f"select lambda must return a str, TableField, Function, or a list of them, not {type(fields).__name__}"
                )

            if not self._select_fields:
                raise ValueError("No fields selected")

            self.logger.debug(
                f"Selected fields: {[repr(f) for f in self._select_fields]}"
            )
            return self
        except TypeError as e:
            self.logger.error(f"Type error in select method: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Validation error in select method: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error in select method: {e}")
            raise
        finally:
            self.logger.debug("'select' method finished.")

    def distinct(
        self, field_lambda: Optional[Callable[[T], TableField]] = None
    ) -> "Query[T]":
        """
        Applies the DISTINCT clause to the query to retrieve unique rows.

        This method can be used in two ways:
        1. To retrieve rows with unique combinations of all selected columns (using `distinct()`).
        2. To retrieve the first row for each distinct value of a specified column (using `distinct_on(column)`).

        Use Cases:
        1. Get all unique rows based on all selected columns:
           ```python
           query.distinct()
           ```

        2. Get the first row for each unique value in the 'category' column:
           ```python
           query.distinct(lambda t: t.category)
           ```

        3. Applying `distinct` after selecting specific columns to get unique combinations of those columns:
            ```python
            query.select(lambda t: [t.city, t.zip_code]).distinct()
            ```

        4. Applying `distinct_on` after selecting specific columns (the distinct will still be based on the `distinct_on` column):
            ```python
            query.select(lambda t: [t.city, t.zip_code]).distinct(lambda t: t.city)
            ```

        5. Using `distinct` on a query that already has a WHERE clause:
            ```python
            query.where(lambda t: t.is_active == True).distinct()
            ```

        6. Using `distinct_on` on a query that already has a WHERE clause:
            ```python
            query.where(lambda t: t.status == 'pending').distinct(lambda t: t.customer_id)
            ```

        7. Applying `distinct` to a query with a LIMIT (the DISTINCT operation happens before the LIMIT):
            ```python
            query.distinct().limit(10)
            ```

        8. Applying `distinct_on` to a query with an OFFSET:
            ```python
            query.distinct(lambda t: t.group_id).offset(5)
            ```

        9. Using `distinct` in a subquery (syntax might vary depending on your ORM's subquery implementation):
            ```python
            # Example conceptual syntax
            subquery = Query[User](User.__tablename__, User, db, logger).select(lambda t: t.region).distinct()
            subquery = Subquery(subquery=subquery)
            main_query.where(lambda m: m.region.in_(subquery))
            ```

        10. Using `distinct` when selecting a single column (equivalent to `SELECT DISTINCT column FROM table`):
            ```python
            query.select(lambda t: t.role).distinct()
            ```
        """
        self.logger.debug("Entering distinct method.")
        try:
            if field_lambda is None:
                self._distinct = True
                self.logger.debug("Set to DISTINCT (all columns).")
            else:
                if not callable(field_lambda):
                    raise TypeError("field_lambda must be a callable")

                table = Table()
                field = field_lambda(table)
                if not isinstance(field, TableField):
                    raise TypeError(
                        f"distinct lambda must return a TableField, not {type(field).__name__}"
                    )
                self._distinct_on = field
                self.logger.debug(f"Set to DISTINCT ON column: {field.name}")
            return self
        except TypeError as e:
            self.logger.error(f"Type error in distinct method: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error in distinct method: {e}")
            raise
        finally:
            self.logger.debug("'distinct' method finished.")

    def where(self, where_lambda: Callable[[T], Expression]) -> "Query[T]":
        """
        Adds a WHERE clause to the query to filter results.

        The `where_lambda` argument should be a callable that accepts a single
        argument (representing the table object) and returns an `Expression`
        object representing the filter condition. Multiple `where` calls will
        be combined with the AND operator.

        Use Cases:
        1. Filtering by equality on a single column:
           ```python
           query.where(lambda t: t.id == 1)
           ```

        2. Filtering by inequality on a single column:
           ```python
           query.where(lambda t: t.status != 'pending')
           ```

        3. Filtering with the less than operator:
           ```python
           query.where(lambda t: t.age < 30)
           ```

        4. Filtering with the greater than operator:
           ```python
           query.where(lambda t: t.price > 100.00)
           ```

        5. Filtering with the less than or equal to operator:
           ```python
           query.where(lambda t: t.quantity <= 5)
           ```

        6. Filtering with the greater than or equal to operator:
           ```python
           query.where(lambda t: t.score >= 90)
           ```

        7. Filtering with the IN operator for a list of values:
           ```python
           query.where(lambda t: t.category.in_(['A', 'B', 'C']))
           ```

        8. Filtering with the NOT IN operator for a list of values:
           ```python
           query.where(lambda t: t.country.not_in(['USA', 'Canada']))
           ```

        9. Filtering with the LIKE operator for pattern matching:
           ```python
           query.where(lambda t: t.name.like('John%'))
           ```

        10. Filtering with the NOT LIKE operator:
            ```python
            query.where(lambda t: t.email.not_like('%@example.com'))
            ```

        11. Filtering with the IS NULL method:
            ```python
            query.where(lambda t: t.description.is_null())
            ```

        12. Filtering with the IS NOT NULL operator:
            ```python
            query.where(lambda t: t.updated_at.is_not_null())
            # or using invert operator
            query.where(lambda t: ~t.updated_at.is_null())
            ```

        13. Combining multiple conditions with AND (by calling `where` multiple times):
            ```python
            query.where(lambda t: t.is_active == True).where(lambda t: t.role == 'admin')
            ```

        14. Combining multiple conditions with OR:
            ```python
            query.where(lambda t: (t.status == 'active') | (t.status == 'pending'))
            ```

        15. Filtering by a date range:
            ```python
            from datetime import datetime
            start_date = datetime(2023, 1, 1)
            end_date = datetime(2023, 1, 31)
            query.where(lambda t: t.order_date >= start_date).where(lambda t: t.order_date <= end_date)
            ```

        16. Filtering with a boolean column:
            ```python
            query.where(lambda t: t.is_deleted == False)
            ```

        17. Filtering with multiple IN conditions:
            ```python
            query.where(lambda t: t.color.in_(['red', 'blue'])).where(lambda t: t.size.in_(['S', 'M']))
            ```
        """
        self.logger.debug("Entering where method.")
        try:
            if not callable(where_lambda):
                raise TypeError("where_lambda must be a callable")

            table = Table()
            new_where_clause = where_lambda(table)
            if not isinstance(new_where_clause, Expression):
                raise TypeError(
                    f"where lambda must return an Expression, not {type(new_where_clause).__name__}"
                )
            if self._where_clause is None:
                self._where_clause = new_where_clause
                self.logger.debug(f"Set initial WHERE clause: {self._where_clause}")
            else:
                self._where_clause = Expression(
                    ("AND", self._where_clause, new_where_clause)
                )
                self.logger.debug(
                    f"Combined WHERE clause with AND: {self._where_clause}"
                )
            return self
        except TypeError as e:
            self.logger.error(f"Type error in where method: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error during where lambda execution: {e}")
            raise
        finally:
            self.logger.debug("'where' method finished.")

    def order_by(
        self,
        order_lambda: Callable[[T], TableField],
        order_type: Optional[OrderType] = None,
    ) -> "Query[T]":
        """
        Specifies the ordering of the result set.

        The `order_lambda` argument should be a callable that accepts a single
        argument (representing the table object) and returns a `TableField`
        object indicating the column to order by. The optional `order_type`
        argument, if provided, should be an instance of the `OrderType` enum
        (e.g., `OrderType.ASC` for ascending, `OrderType.DESC` for descending).

        Use Cases:
        1. Order by a single column:
           ```python
           query.order_by(lambda t: t.name)
           ```

        2. Order by a single column in ascending order:
           ```python
           query.order_by(lambda t: t.created_at, order_type=OrderType.ASC)
           ```

        3. Order by a single column in descending order:
           ```python
           query.order_by(lambda t: t.age, order_type=OrderType.DESC)
           ```

        4. Order by a string column:
           ```python
           query.order_by(lambda t: t.email)
           ```

        5. Order by a numeric column in descending order:
           ```python
           query.order_by(lambda t: t.price, order_type=OrderType.DESC)
           ```

        6. Order by a date column:
           ```python
           query.order_by(lambda t: t.order_date)
           ```

        7. Order by a boolean column (database default order for booleans):
           ```python
           query.order_by(lambda t: t.is_active)
           ```

        8. Ordering after applying a WHERE clause:
            ```python
            query.where(lambda t: t.status == 'completed').order_by(lambda t: t.completion_date)
            ```

        9. Ordering after selecting specific columns:
            ```python
            query.select(lambda t: [t.product_name, t.price]).order_by(lambda t: t.price)
            ```

        10. Ordering by a column that is also being selected:
            ```python
            query.select(lambda t: [t.name, t.priority]).order_by(lambda t: t.priority, order_type=OrderType.DESC)
            ```

        11. Ordering results for pagination:
            ```python
            query.order_by(lambda t: t.id).limit(10).offset(20)
            ```
        """
        self.logger.debug("Entering order_by method.")
        try:
            if not callable(order_lambda):
                raise TypeError("order_lambda must be a callable")

            table = Table()
            column = order_lambda(table)
            if not isinstance(column, TableField):
                raise TypeError(
                    f"order_by lambda must return a TableField, not {type(column).__name__}"
                )

            order_str = column.name
            if order_type:
                if not isinstance(order_type, OrderType):
                    raise TypeError(
                        f"order_type must be an instance of OrderType, not {type(order_type).__name__}"
                    )
                order_str += f" {order_type.value}"

            self._order_by_clause = order_str
            self.logger.debug(f"Set ORDER BY clause: {self._order_by_clause}")
            return self
        except TypeError as e:
            self.logger.error(f"Type error in order_by method: {e}")
            raise
        except Exception as e:
            self.logger.critical(
                f"Unexpected error during order_by lambda execution: {e}"
            )
            raise
        finally:
            self.logger.debug("'order_by' method finished.")

    def then_by(
        self,
        then_lambda: Callable[[T], TableField],
        order_type: Optional[OrderType] = None,
    ) -> "Query[T]":
        """
        Specifies subsequent ordering criteria after an initial `order_by`.

        This method is used to add secondary or tertiary ordering to the query
        results. It must be called after the `order_by` method has been used.
        The `then_lambda` argument is a callable that takes the table object
        and returns the `TableField` to order by. The optional `order_type`
        specifies the sort order (ascending or descending).

        Use Cases:
        1. Then by another column:
           ```python
           query.order_by(lambda t: t.category).then_by(lambda t: t.name)
           ```

        2. Then by another column in descending order:
           ```python
           query.order_by(lambda t: t.category).then_by(lambda t: t.price, order_type=OrderType.DESC)
           ```

        3. Multiple `then_by` calls for multi-level sorting:
           ```python
           query.order_by(lambda t: t.country).then_by(lambda t: t.city).then_by(lambda t: t.zip_code)
           ```

        4. Then by a date column:
           ```python
           query.order_by(lambda t: t.user_id).then_by(lambda t: t.registration_date)
           ```

        5. Then by a boolean column:
           ```python
           query.order_by(lambda t: t.priority, order_type=OrderType.DESC).then_by(lambda t: t.is_active)
           ```

        6. Using `then_by` with a specific `OrderType`:
           ```python
           query.order_by(lambda t: t.status).then_by(lambda t: t.modified_at, order_type=OrderType.DESC)
           ```

        7. Then by a foreign key column:
           ```python
           query.order_by(lambda t: t.order_date).then_by(lambda t: t.customer_id)
           ```

        8. Then by a column that was also selected:
           ```python
           query.select(lambda t: [t.group, t.sort_order, t.item_name]).order_by(lambda t: t.group).then_by(lambda t: t.sort_order)
           ```

        9. Then by a column with a common name:
           ```python
           query.order_by(lambda t: t.type).then_by(lambda t: t.value)
           ```

        10. Then by an ID column as a secondary sort:
            ```python
            query.order_by(lambda t: t.name).then_by(lambda t: t.id)
            ```

        11. Then by a different column with descending order:
            ```python
            query.order_by(lambda t: t.department).then_by(lambda t: t.employee_id, order_type=OrderType.DESC)
            ```

        12. Applying `then_by` after a `where` clause:
            ```python
            query.where(lambda t: t.year == 2024).order_by(lambda t: t.month).then_by(lambda t: t.day)
            ```

        13. Applying `then_by` after a `distinct` clause (the ordering happens on the distinct results):
            ```python
            query.distinct(lambda t: t.product_code).order_by(lambda t: t.product_code).then_by(lambda t: t.version, order_type=OrderType.DESC)
            ```

        14. Using `then_by` for more complex sorting scenarios:
            ```python
            query.order_by(lambda t: t.is_premium, order_type=OrderType.DESC).then_by(lambda t: t.signup_date)
            ```

        15. Then by a column that is not the primary sort key:
            ```python
            query.order_by(lambda t: t.relevance_score, order_type=OrderType.DESC).then_by(lambda t: t.publish_date, order_type=OrderType.DESC)
            ```

        16. Using `then_by` multiple times with different order types:
            ```python
            query.order_by(lambda t: t.event_date).then_by(lambda t: t.start_time).then_by(lambda t: t.duration, order_type=OrderType.DESC)
            ```

        17. Then by a column that might have null values (database's default null sorting applies):
            ```python
            query.order_by(lambda t: t.optional_field).then_by(lambda t: t.required_field)
            ```
        """
        self.logger.debug("Entering then_by method.")
        try:
            if not self._order_by_clause:
                raise ValueError("then_by method must be called after order_by")

            if not callable(then_lambda):
                raise TypeError("then_lambda must be a callable")

            table = Table()
            column = then_lambda(table)
            if not isinstance(column, TableField):
                raise TypeError(
                    f"then_by lambda must return a TableField, not {type(column).__name__}"
                )

            self._order_by_clause += f", {column.name}"
            if order_type:
                if not isinstance(order_type, OrderType):
                    raise TypeError(
                        f"order_type must be an instance of OrderType, not {type(order_type).__name__}"
                    )
                self._order_by_clause += f" {order_type.value}"

            log_message = f"Then by column: {column.name}"
            if order_type:
                log_message += f" {order_type.value}"
            self.logger.debug(log_message)
            return self
        except ValueError as e:
            self.logger.error(f"Validation error in then_by method: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Type error in then_by method: {e}")
            raise
        except Exception as e:
            self.logger.critical(
                f"Unexpected error during then_by lambda execution: {e}"
            )
            raise
        finally:
            self.logger.debug("'then_by' method finished.")

    def range(self, start: int, end: int) -> "Query[T]":
        """
        Specifies a range of rows to retrieve from the result set using offset and limit.

        This method is a convenience for setting both the starting row (offset)
        and the number of rows to retrieve (limit) in a single call. The `start`
        parameter defines the zero-based index of the first row to return, and
        the `end` parameter defines the index of the row after the last row to
        return. Therefore, the number of rows returned will be `end - start`.

        Use Cases:
        1. Get rows 1 to 10 (inclusive):
           ```python
           query.range(0, 10)
           ```

        2. Get the next 10 rows starting from row 11:
           ```python
           query.range(10, 20)
           ```

        3. Get a small subset of data for testing:
           ```python
           query.range(5, 8) # Returns rows 6, 7, 8
           ```

        4. Implementing basic pagination (first page, 10 items per page):
           ```python
           page_number = 1
           page_size = 10
           start_index = (page_number - 1) * page_size
           end_index = start_index + page_size
           query.range(start_index, end_index)
           ```

        5. Implementing pagination (second page, 10 items per page):
           ```python
           page_number = 2
           page_size = 10
           start_index = (page_number - 1) * page_size
           end_index = start_index + page_size
           query.range(start_index, end_index) # range(10, 20)
           ```

        6. Getting the last few rows (requires knowing the total count beforehand and careful calculation):
           ```python
           # Assuming total_rows is known
           total_rows = 100
           last_few = 5
           start_index = total_rows - last_few
           end_index = total_rows
           query.range(start_index, end_index) # range(95, 100)
           ```

        7. Using `range` after applying a `where` clause:
           ```python
           query.where(lambda t: t.category == 'books').range(0, 5)
           ```

        8. Using `range` after applying an `order_by` clause:
           ```python
           query.order_by(lambda t: t.price, order_type=OrderType.DESC).range(0, 3) # Get the top 3 most expensive items
           ```

        9. Combining `range` with `distinct` (range is applied to the distinct results):
            ```python
            query.distinct(lambda t: t.email).range(0, 15) # Get the first 15 unique emails
            ```

        10. Getting a single row (the third row):
            ```python
            query.range(2, 3) # Returns only the row at index 2
            ```

        11. Getting the first N rows (equivalent to `limit(N)` if start is 0):
            ```python
            n = 25
            query.range(0, n)
            ```

        12. Applying `range` after multiple `where` and `order_by` calls:
            ```python
            query.where(lambda t: t.status == 'active').where(lambda t: t.country == 'US').order_by(lambda t: t.signup_date).range(0, 50)
            ```

        13. Getting a specific segment of a log or audit trail:
            ```python
            query.order_by(lambda t: t.timestamp).range(1000, 1050)
            ```
        """
        self.logger.debug("Entering range method.")
        try:
            if not isinstance(start, int):
                raise TypeError(f"start must be an integer, not {type(start).__name__}")
            if start < 0:
                raise ValueError("start must be a non-negative integer")

            if not isinstance(end, int):
                raise TypeError(f"end must be an integer, not {type(end).__name__}")
            if end <= start:
                raise ValueError("end must be greater than start")

            self._offset_clause = start
            self._limit_clause = end - start
            self.logger.debug(f"Set range: offset={start}, limit={self._limit_clause}")
            return self
        except TypeError as e:
            self.logger.error(f"Type error in range method: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Validation error in range method: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error in range method: {e}")
            raise
        finally:
            self.logger.debug("'range' method finished.")

    def limit(self, count: int) -> "Query[T]":
        """
        Limits the number of rows returned by the query.

        The `count` parameter specifies the maximum number of rows that the
        query should return. This is useful for pagination and for retrieving
        only a subset of the results.

        Use Cases:
        1. Limit the result to the first 10 rows:
           ```python
           query.limit(10)
           ```

        2. Get only the top 5 results after ordering:
           ```python
           query.order_by(lambda t: t.score, order_type=OrderType.DESC).limit(5)
           ```

        3. Implement basic pagination (get the first page with 20 items):
           ```python
           page_size = 20
           query.limit(page_size)
           ```

        4. Get a small sample of data:
           ```python
           query.limit(3)
           ```

        5. Limit the results after applying a WHERE clause:
           ```python
           query.where(lambda t: t.is_active == True).limit(15)
           ```

        6. Limit the results of a distinct query:
           ```python
           query.distinct(lambda t: t.category).limit(7)
           ```

        7. Get the single most recent entry:
           ```python
           query.order_by(lambda t: t.created_at, order_type=OrderType.DESC).limit(1)
           ```

        8. Limit the results in conjunction with an offset (for pagination):
           ```python
           page_number = 3
           page_size = 10
           offset = (page_number - 1) * page_size
           query.offset(offset).limit(page_size)
           ```

        9. Get the top N performing items:
           ```python
           n = 25
           query.order_by(lambda t: t.performance, order_type=OrderType.DESC).limit(n)
           ```

        10. Limit the number of unique items:
            ```python
            query.distinct(lambda t: t.product_id).limit(30)
            ```

        11. Get a limited number of records for processing:
            ```python
            query.where(lambda t: t.needs_processing == True).limit(100)
            ```

        12. Limit results to a reasonable number to avoid performance issues on large tables:
            ```python
            query.limit(1000)
            ```

        13. Get the first few examples for a demo:
            ```python
            query.limit(4)
            ```

        14. Limit results based on a configuration setting:
            ```python
            max_results = get_config('max_search_results')
            query.limit(max_results)
            ```

        15. Limiting results for a specific user or group:
            ```python
            user_id = get_current_user_id()
            query.where(lambda t: t.user_id == user_id).limit(50)
            ```
        """
        self.logger.debug("Entering limit method.")
        try:
            if not isinstance(count, int):
                raise TypeError(f"count must be an integer, not {type(count).__name__}")
            if count <= 0:
                raise ValueError("limit must be a positive integer")

            self._limit_clause = count
            self.logger.debug(f"Set limit: {count}")
            return self
        except TypeError as e:
            self.logger.error(f"Type error in limit method: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Validation error in limit method: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error in limit method: {e}")
            raise
        finally:
            self.logger.debug("'limit' method finished.")

    def offset(self, count: int) -> "Query[T]":
        """
        Specifies the number of rows to skip before starting to return rows.

        The `count` parameter determines how many initial rows from the result
        set should be skipped. This is commonly used for implementing pagination.
        The offset is zero-based.

        Use Cases:
        1. Skip the first 10 rows:
           ```python
           query.offset(10)
           ```

        2. Implement pagination (get the second page with a page size of 10):
           ```python
           page_number = 2
           page_size = 10
           offset = (page_number - 1) * page_size
           query.offset(offset) # offset(10)
           ```

        3. Skip a larger number of initial rows:
           ```python
           query.offset(50)
           ```

        4. Get results starting from a specific row number:
           ```python
           start_from_row = 25
           query.offset(start_from_row - 1) # Adjust to zero-based index
           ```

        5. Use `offset` after applying a `where` clause:
           ```python
           query.where(lambda t: t.category == 'electronics').offset(5)
           ```

        6. Use `offset` after applying an `order_by` clause:
           ```python
           query.order_by(lambda t: t.price).offset(20) # Skip the 20 cheapest items
           ```

        7. Combine `offset` with `limit` for pagination (get the third page with a page size of 15):
           ```python
           page_number = 3
           page_size = 15
           offset = (page_number - 1) * page_size
           query.offset(offset).limit(page_size) # offset(30).limit(15)
           ```

        8. Skip the initial results of a distinct query:
           ```python
           query.distinct(lambda t: t.user_id).offset(5) # Skip the first 5 unique user IDs
           ```

        9. Offset by a small amount to get a slightly later set of results:
           ```python
           query.offset(3)
           ```

        10. Offset by a larger amount in a large dataset:
            ```python
            query.offset(1000)
            ```

        11. Implement "load more" functionality (skip the items already loaded):
            ```python
            items_loaded = 30
            query.offset(items_loaded)
            ```

        12. Offset in a subquery (the offset applies to the subquery's results):
            ```python
            # Example conceptual syntax
            # subquery = Query(...).offset(5).select(...)
            pass # Assuming subquery logic is handled elsewhere
            ```

        13. Skip the first few entries in a sorted list:
            ```python
            query.order_by(lambda t: t.name).offset(8)
            ```

        14. Offset based on a dynamic page number:
            ```python
            current_page = get_current_page_number()
            page_size = 25
            offset = (current_page - 1) * page_size
            query.offset(offset)
            ```

        15. Skip a certain number of records based on a user preference:
            ```python
            skip_count = get_user_preference('results_to_skip')
            query.offset(skip_count)
            ```

        16. Offset after multiple `where` and `order_by` clauses:
            ```python
            query.where(lambda t: t.status == 'processed').order_by(lambda t: t.completion_time).offset(100)
            ```

        17. Offset the results of a query with a limit:
            ```python
            query.limit(50).offset(25) # Get rows 26 to 50
            ```

        18. Implement a "next page" button functionality:
            ```python
            current_offset = get_current_offset()
            page_size = 10
            next_offset = current_offset + page_size
            query.offset(next_offset)
            ```

        19. Skip a specific number of log entries:
            ```python
            query.order_by(lambda t: t.timestamp).offset(500)
            ```

        20. Offset the results of a query with a complex filtering and ordering:
            ```python
            query.where(lambda t: t.category.in_(['a', 'b'])).order_by(lambda t: t.value, order_type=OrderType.DESC).offset(10)
            ```
        """
        self.logger.debug("Entering offset method.")
        try:
            if not isinstance(count, int):
                raise TypeError(f"count must be an integer, not {type(count).__name__}")
            if count < 0:
                raise ValueError("offset must be a non-negative integer")

            self._offset_clause = count
            self.logger.debug(f"Set offset: {count}")
            return self
        except TypeError as e:
            self.logger.error(f"Type error in offset method: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Validation error in offset method: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error in offset method: {e}")
            raise
        finally:
            self.logger.debug("'offset' method finished.")

    def group_by(
        self,
        fields_lambda: Callable[
            [T], Union[str, TableField, List[TableField], List[str]]
        ],
    ) -> "Query[T]":
        """
        Specifies the columns to group the result set by.

        This method is used to group rows that have the same values in one or
        more columns into a summary row, like "find the number of customers
        in each city". It is often used with aggregate functions (e.g., `count`,
        `avg`, `sum`). The `fields_lambda` should return a single `str` or
        `TableField`, or a list of them, representing the columns to group by.

        Use Cases:
        1. Group by a single column (string):
           ```python
           query.group_by(lambda t: "city")
           ```

        2. Group by a single column (TableField):
           ```python
           query.group_by(lambda t: t.status)
           ```

        3. Group by multiple columns (list of strings):
           ```python
           query.group_by(lambda t: ["country", "region"])
           ```

        4. Group by multiple columns (list of TableFields):
           ```python
           query.group_by(lambda t: [t.category, t.sub_category])
           ```

        5. Group by after selecting aggregate functions:
           ```python
           query.select(lambda t: [t.city, func.count(t.user_id)]).group_by(lambda t: t.city)
           ```

        6. Group by with a WHERE clause applied beforehand:
           ```python
           query.where(lambda t: t.is_active == True).group_by(lambda t: t.age_group)
           ```

        7. Group by and then order the results:
           ```python
           query.group_by(lambda t: t.product_type).order_by(lambda t: t.product_type)
           ```

        8. Group by multiple fields and then order:
           ```python
           query.group_by(lambda t: ["order_date", "customer_id"]).order_by(lambda t: t.order_date)
           ```

        9. Group by a foreign key column:
           ```python
           query.group_by(lambda t: t.user_id)
           ```

        10. Group by a date column (e.g., to count events per day):
            ```python
            query.group_by(lambda t: t.event_date)
            ```

        11. Group by a boolean column (e.g., to count active vs. inactive users):
            ```python
            query.group_by(lambda t: t.is_premium)
            ```

        12. Group by a column with a limited number of distinct values:
            ```python
            query.group_by(lambda t: t.browser)
            ```

        13. Grouping results for generating reports:
            ```python
            query.group_by(lambda t: t.reporting_period)
            ```

        14. Grouping data for statistical analysis:
            ```python
            query.group_by(lambda t: t.experiment_group)
            ```

        15. Grouping by a combination of categorical variables:
            ```python
            query.group_by(lambda t: [t.gender, t.education_level])
            ```

        16. Grouping results before applying a limit (the grouping happens first):
            ```python
            query.group_by(lambda t: t.category).limit(5) # Get counts for the first 5 categories (order not guaranteed without order_by)
            ```

        17. Grouping results and then filtering the groups with `having` (if your ORM supports it):
            ```python
            # Example conceptual syntax for having
            # query.group_by(lambda t: t.department).having(lambda g: func.count(g.employee_id) > 10)
            query.group_by(lambda t: t.department) # Basic group_by
            ```

        18. Grouping by a column that is also used in an aggregate function (this is common):
            ```python
            query.group_by(lambda t: t.product_id).select(lambda t: [t.product_id, func.sum(t.sales)])
            ```

        19. Grouping by a column that is selected without aggregation:
            ```python
            query.select(lambda t: [t.region]).group_by(lambda t: t.region)
            ```

        20. Grouping by a column with potential null values (null is treated as a distinct group):
            ```python
            query.group_by(lambda t: t.optional_field)
            ```
        """
        self.logger.debug("Entering group_by method.")
        self._group_by_fields = []  # Clear previous fields on each group_by call
        try:
            if not callable(fields_lambda):
                raise TypeError("fields_lambda must be a callable")

            table = Table()
            fields = fields_lambda(table)

            if fields is None:
                raise ValueError("fields lambda cannot return None")

            if isinstance(fields, list):
                if not fields:
                    raise ValueError("fields lambda returned an empty list")
                for field in fields:
                    if isinstance(field, str):
                        self._group_by_fields.append(TableField(field.strip()))
                    elif isinstance(field, TableField):
                        self._group_by_fields.append(field)
                    else:
                        raise TypeError(
                            f"Elements in group_by list must be str or TableField not {type(field).__name__}"
                        )
            elif isinstance(fields, str):
                self._group_by_fields.append(TableField(fields.strip()))
            elif isinstance(fields, TableField):
                self._group_by_fields.append(fields)
            else:
                raise TypeError(
                    f"fields lambda must return a str, TableField, or a list of them, not {type(fields).__name__}"
                )

            if not self._group_by_fields:
                raise ValueError("No fields provided for grouping")

            self.logger.debug(
                f"Set GROUP BY fields: {[f.name for f in self._group_by_fields]}"
            )
            return self
        except TypeError as e:
            self.logger.error(f"Type error in group_by method: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Validation error in group_by method: {e}")
            raise
        except Exception as e:
            self.logger.critical(
                f"Unexpected error during group_by lambda execution: {e}"
            )
            raise
        finally:
            self.logger.debug("'group_by' method finished.")

    def compile(self) -> Tuple[str, List[Any]]:
        """
        Compiles the query into an SQL string and a list of arguments.

        This method takes all the previously specified clauses (SELECT, DISTINCT,
        WHERE, GROUP BY, ORDER BY, LIMIT, OFFSET) and combines them into a
        valid SQL query string. It also collects any arguments that need to be
        passed to the database driver for parameter binding, preventing SQL
        injection vulnerabilities.

        Use Cases:
        1. Compile a basic SELECT * query:
           ```python
           query.compile()
           # Output: ('SELECT * FROM your_table_name', [])
           ```

        2. Compile a query with specific selected fields:
           ```python
           query.select(lambda t: [t.name, t.email]).compile()
           # Output: ('SELECT name, email FROM your_table_name', [])
           ```

        3. Compile a query with a WHERE clause:
           ```python
           query.where(lambda t: t.id == 10).compile()
           # Output: ('SELECT * FROM your_table_name WHERE id = ?', [10])
           ```

        4. Compile a query with ORDER BY:
           ```python
           query.order_by(lambda t: t.created_at, order_type=OrderType.DESC).compile()
           # Output: ('SELECT * FROM your_table_name ORDER BY created_at DESC', [])
           ```

        5. Compile a query with LIMIT:
           ```python
           query.limit(5).compile()
           # Output: ('SELECT * FROM your_table_name LIMIT 5', [])
           ```

        6. Compile a query with OFFSET:
           ```python
           query.offset(10).compile()
           # Output: ('SELECT * FROM your_table_name OFFSET 10', [])
           ```

        7. Compile a query with DISTINCT:
           ```python
           query.distinct().compile()
           # Output: ('SELECT DISTINCT * FROM your_table_name', [])
           ```

        8. Compile a query with DISTINCT ON a column:
           ```python
           query.distinct(lambda t: t.category).compile()
           # Output: ('SELECT DISTINCT ON (category) * FROM your_table_name', [])
           ```

        9. Compile a query with GROUP BY:
           ```python
           query.group_by(lambda t: t.city).compile()
           # Output: ('SELECT * FROM your_table_name GROUP BY city', [])
           ```

        10. Compile a query with multiple clauses:
            ```python
            query.select(lambda t: [t.name, t.age]).where(lambda t: t.age > 25).order_by(lambda t: t.name).limit(10).offset(5).compile()
            # Output: ('SELECT name, age FROM your_table_name WHERE age > ? ORDER BY name LIMIT ? OFFSET ?', [25, 10, 5])
            ```

        11. Compile a query selecting a function:
            ```python
            query.select(lambda t: func.count(t.id).label('user_count')).group_by(lambda t: t.status).compile()
            # Output: ('SELECT count(id) AS user_count FROM your_table_name GROUP BY status', [])
            ```

        12. Compile a query with IN condition in WHERE clause:
            ```python
            query.where(lambda t: t.status.in_(['active', 'pending'])).compile()
            # Output: ('SELECT * FROM your_table_name WHERE status IN (?, ?)', ['active', 'pending'])
            ```

        13. Compile a query with LIKE condition:
            ```python
            query.where(lambda t: t.email.like('%@example.com')).compile()
            # Output: ('SELECT * FROM your_table_name WHERE email LIKE ?', ['%@example.com'])
            ```

        14. Compile a query with IS NULL condition:
            ```python
            query.where(lambda t: t.description == None).compile()
            # Output: ('SELECT * FROM your_table_name WHERE description IS NULL', [])
            ```

        15. Compile a query with a `then_by` clause:
            ```python
            query.order_by(lambda t: t.category).then_by(lambda t: t.name).compile()
            # Output: ('SELECT * FROM your_table_name ORDER BY category, name', [])
            ```

        16. Compile a query using the `range` method:
            ```python
            query.range(5, 15).compile()
            # Output: ('SELECT * FROM your_table_name LIMIT ? OFFSET ?', [10, 5])
            ```

        17. Compile a query with a complex WHERE clause involving AND/OR (assuming `Expression` handles this):
            ```python
            # Assuming Expression can be constructed for complex logic
            # query.where(lambda t: (t.age > 30) & (t.city == 'New York') | (t.is_premium == True)).compile()
            query.where(lambda t: True).compile() # Placeholder for complex expression compilation
            # Output would depend on how the Expression is compiled
            ```

        18. Compile a query with a subquery in the SELECT clause (if supported by `compile_expression`):
            ```python
            # Output depends on the implementation of subquery compilation
            query.select(lambda t: [t.name, "(SELECT COUNT(*) FROM other_table WHERE ...)"]).compile()
            # Output would be a string with the subquery embedded
            ```

        19. Compile a query with a subquery in the WHERE clause:
            ```python
            # Output depends on the implementation of subquery compilation
            # query.where(lambda t: t.id.in_((Query(...).select(lambda s: s.item_id)))).compile()
            query.where(lambda t: True).compile() # Placeholder for subquery compilation
            # Output would include the subquery SQL
            ```

        20. Compile a query that selects all fields and applies a simple limit:
            ```python
            query.limit(20).compile()
            # Output: ('SELECT * FROM your_table_name LIMIT 20', [])
            ```
        """
        self.logger.debug("Entering compile method.")
        self._query_args = []
        query_parts: List[str] = ["SELECT"]

        # DISTINCT
        if self._distinct:
            query_parts.append("DISTINCT")
        elif self._distinct_on:
            distinct_expression_str = compile_expression(
                self._distinct_on, self._query_args
            )
            query_parts.append(f"DISTINCT ON ({distinct_expression_str})")

        # SELECT
        if self._select_fields:
            select_columns = [
                compile_expression(field, self._query_args)
                for field in self._select_fields
            ]
            query_parts.append(", ".join(select_columns))
        else:
            query_parts.append("*")

        # FROM
        query_parts.append(f"FROM {self.table_name}")

        # WHERE
        if self._where_clause:
            where_clause_str = compile_expression(self._where_clause, self._query_args)
            query_parts.append(f"WHERE {where_clause_str}")

        # GROUP BY
        if self._group_by_fields:
            group_by_columns = [
                compile_expression(field, self._query_args)
                for field in self._group_by_fields
            ]
            query_parts.append("GROUP BY " + ", ".join(group_by_columns))

        # ORDER BY
        if self._order_by_clause:
            query_parts.append(f"ORDER BY {self._order_by_clause}")

        # LIMIT
        if self._limit_clause is not None:
            if not isinstance(self._limit_clause, int) or self._limit_clause < 0:
                error_msg = f"Invalid limit value: {self._limit_clause}. Must be a positive integer."
                self.logger.error(error_msg)
                raise ValueError(error_msg)
            query_parts.append(f"LIMIT {self._limit_clause}")

        # OFFSET
        if self._offset_clause is not None:
            if not isinstance(self._offset_clause, int) or self._offset_clause < 0:
                error_msg = f"Invalid offset value: {self._offset_clause}. Must be a non-negative integer."
                self.logger.error(error_msg)
                raise ValueError(error_msg)
            query_parts.append(f"OFFSET {self._offset_clause}")

        compiled_query = " ".join(query_parts)
        self.logger.debug(
            f"Compiled SQL: {compiled_query}, Arguments: {self._query_args}"
        )
        return compiled_query, self._query_args

    async def run(self) -> str:
        """
        Asynchronously executes the compiled SQL query against the database.

        This method compiles the query built using the fluent interface
        (`select`, `where`, `order_by`, etc.) into an SQL string and its
        arguments. It then executes this SQL against the database using the
        provided database connection (`self.db`). The result of the execution
        is returned as a string (the exact format depends on the database
        driver and the type of query executed).

        Use Cases:
        1. Execute a simple SELECT * query:
           ```python
           result = await query.run()
           # result will contain all rows and columns from the table
           ```

        2. Execute a query with specific selected fields:
           ```python
           result = await query.select(lambda t: [t.name, t.email]).run()
           # result will contain only the name and email columns
           ```

        3. Execute a query with a WHERE clause to filter results:
           ```python
           result = await query.where(lambda t: t.status == 'active').run()
           # result will contain only the active records
           ```

        4. Execute a query with ordering:
           ```python
           result = await query.order_by(lambda t: t.created_at, order_type=OrderType.DESC).run()
           # result will be ordered by creation date descending
           ```

        5. Execute a query with a limit on the number of rows returned:
           ```python
           result = await query.limit(10).run()
           # result will contain at most 10 rows
           ```

        6. Execute a query with an offset to skip initial rows:
           ```python
           result = await query.offset(20).run()
           # result will skip the first 20 rows
           ```

        7. Execute a query to get unique rows:
           ```python
           result = await query.distinct().run()
           # result will contain only unique rows
           ```

        8. Execute a query to get unique values for a specific column:
           ```python
           result = await query.distinct(lambda t: t.category).select(lambda t: [t.category]).run()
           # result will contain unique category values
           ```

        9. Execute a query with grouping:
           ```python
           result = await query.group_by(lambda t: t.city).select(lambda t: [t.city, func.count(t.user_id)]).run()
           # result will contain counts of users per city
           ```

        10. Execute a query with all clauses combined:
            ```python
            result = await query.select(lambda t: [t.name, t.age]).where(lambda t: t.age > 25).order_by(lambda t: t.name).limit(10).offset(5).run()
            # result will be a paginated, filtered, and ordered list of names and ages
            ```

        11. Execute a query that involves database functions:
            ```python
            result = await query.select(lambda t: func.avg(t.score)).run()
            # result will contain the average score
            ```

        12. Execute a query with parameters in the WHERE clause (handled by compilation):
            ```python
            result = await query.where(lambda t: t.email == 'test@example.com').run()
            # Safe execution with parameter binding
            ```

        13. Execute a query that returns a single row (e.g., after limiting to 1):
            ```python
            result = await query.where(lambda t: t.id == 1).limit(1).run()
            # result will contain the record with ID 1
            ```

        14. Execute a query and handle potential database errors:
            ```python
            try:
                result = await query.run()
                # Process result
            except PostgresError as e:
                print(f"Database operation failed: {e}")
            ```

        15. Execute a query for reporting purposes:
            ```python
            result = await query.group_by(lambda t: t.report_date).select(lambda t: [t.report_date, func.sum(t.value)]).run()
            # Result set for a time-series report
            ```

        16. Execute a query for data analysis:
            ```python
            result = await query.group_by(lambda t: t.experiment_group).select(lambda t: [t.experiment_group, func.avg(t.outcome)]).run()
            # Results for comparing experiment outcomes
            ```

        17. Execute a query with complex filtering logic:
            ```python
            # Assuming Expression handles complex AND/OR
            # result = await query.where(lambda t: (t.status == 'A') | ((t.status == 'B') & (t.priority > 5))).run()
            result = await query.where(lambda t: True).run() # Placeholder
            ```

        18. Execute a query that might return no results:
            ```python
            result = await query.where(lambda t: t.non_existent_column == 'value').run()
            # result will likely be an empty set or None depending on the driver
            ```

        19. Execute the same query multiple times with different parameters (re-run the query object):
            ```python
            query = Query(...)
            await query.where(lambda t: t.category == 'books').run()
            await query.where(lambda t: t.category == 'movies').run()
            ```

        20. Execute a query and process the raw result from the database driver:
            ```python
            raw_data = await query.run()
            # Further processing of the raw database output
            ```
        """
        self.logger.debug("Entering run method.")
        try:
            sql, args = self.compile()
            self.logger.info(f"Executing SQL: {sql}, Args: {args}")
            result = await self.db.execute(sql, *args)
            self.logger.debug(f"'run' method result: {result}")
            return result
        except ValueError as e:
            self.logger.error(f"Invalid argument in 'run' method: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Invalid type in 'run' method: {e}")
            raise
        except PostgresError as e:
            self.logger.error(f"Database error during 'run': {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error in 'run' method: {e}")
            raise
        finally:
            self.logger.debug("'run' method finished.")

    async def get_one(self) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Asynchronously retrieves exactly one row from the database.

        This method compiles and executes the query, limiting the result set
        to a single row. It returns either an instance of the associated model
        (if one is defined) or a dictionary representing the row. If no matching
        row is found, it returns `None`.

        Use Cases:
        1. Get a single record by its primary key:
           ```python
           user = await query.where(lambda t: t.id == 1).get_one()
           # Returns the User object with id=1 or None
           ```

        2. Get the first record matching a specific condition:
           ```python
           item = await query.where(lambda t: t.status == 'pending').get_one()
           # Returns the first pending item or None
           ```

        3. Get a single record after ordering (e.g., the latest entry):
           ```python
           log = await query.order_by(lambda t: t.timestamp, order_type=OrderType.DESC).get_one()
           # Returns the most recent log entry or None
           ```

        4. Check if a record with specific criteria exists (returns None if not):
           ```python
           user = await query.where(lambda t: t.username == 'unique_user').get_one()
           if user:
               print("User exists")
           else:
               print("User does not exist")
           ```

        5. Retrieve a single configuration setting:
           ```python
           setting = await query.where(lambda t: t.key == 'max_attempts').get_one()
           # Returns the setting record or None
           ```

        6. Get one unique record based on a distinct value:
           ```python
           unique_email = await query.distinct(lambda t: t.email).get_one()
           # Returns one record with a unique email or None
           ```

        7. Retrieve a single row after a group by (the result might be an aggregate):
           ```python
           average_age = await query.group_by(lambda t: t.city).select(lambda t: func.avg(t.age).label('avg_age')).where(lambda t: t.city == 'London').get_one()
           # Returns a dict with the average age in London or None
           ```

        8. Get the first row from a limited set:
           ```python
           first_of_few = await query.limit(5).get_one()
           # Returns the first of the top 5 records or None
           ```

        9. Retrieve a single record after skipping some initial rows:
           ```python
           record_at_offset = await query.offset(10).get_one()
           # Returns the record at index 10 or None
           ```

        10. Get a single record based on a complex WHERE clause:
            ```python
            item = await query.where(lambda t: (t.category == 'electronics') & (t.price < 500)).get_one()
            # Returns one matching electronic item under $500 or None
            ```

        11. Retrieve a single user with a specific role:
            ```python
            admin_user = await query.where(lambda t: t.role == 'admin').get_one()
            # Returns one admin user or None
            ```

        12. Get the most recently updated record of a certain type:
            ```python
            latest_update = await query.where(lambda t: t.type == 'status_update').order_by(lambda t: t.updated_at, order_type=OrderType.DESC).get_one()
            # Returns the latest status update or None
            ```

        13. Check if a specific combination of fields exists:
            ```python
            existing_entry = await query.where(lambda t: (t.field1 == 'value1') & (t.field2 == 'value2')).get_one()
            # Returns the matching record or None
            ```

        14. Retrieve a single record based on a value in a related table (if joins are supported):
            ```python
            # Assuming a join is implicitly handled or via a relation
            # user_with_order = await query.where(lambda u: u.orders.any(order_id=123)).get_one()
            user_with_order = await query.where(lambda t: True).get_one() # Placeholder
            ```

        15. Get the first of a set of records after applying a more complex ordering:
            ```python
            first_sorted = await query.order_by(lambda t: t.priority, order_type=OrderType.DESC).then_by(lambda t: t.name).get_one()
            # Returns the top priority record (and alphabetically first among ties) or None
            ```

        16. Retrieve a single aggregated value (if get_one is used on an aggregation query):
            ```python
            max_price = await query.select(lambda t: func.max(t.price)).get_one()
            # Returns a dict with the max price or None
            ```

        17. Get a single record based on a condition involving a function:
            ```python
            # Assuming a function like lower is available in expressions
            # user = await query.where(lambda t: func.lower(t.username) == 'lowercase').get_one()
            user = await query.where(lambda t: True).get_one() # Placeholder
            ```

        18. Attempt to retrieve a non-existent record (should return None):
            ```python
            non_existent = await query.where(lambda t: t.id == 9999).get_one()
            # Returns None
            ```

        19. Get the single result from a query that is expected to return only one row:
            ```python
            system_status = await query.where(lambda t: t.type == 'system').get_one()
            # Returns the system status record or None
            ```

        20. Retrieve a single record after applying a range (will get the first within that range):
            ```python
            record_in_range = await query.range(5, 10).get_one()
            # Returns the record at index 5 or None
            ```
        """
        self.logger.debug("Entering get_one method.")
        try:
            self._limit_clause = 1
            sql, args = self.compile()
            self.logger.info(f"Executing SQL for get_one(): {sql}, Args: {args}")
            row = await self.db.fetchrow(sql, *args)
            if row:
                return (
                    self.model(**dict(row)) if self._can_return_model() else dict(row)
                )
            return None
        except ValueError as e:
            self.logger.error(f"Invalid argument in 'get_one' method: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Invalid type in 'get_one' method: {e}")
            raise
        except PostgresError as e:
            self.logger.error(f"Database error during 'get_one': {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error in 'get_one': {e}")
            raise
        finally:
            self.logger.debug("'get_one' method finished.")

    async def get_all(self) -> List[Union[T, Dict[str, Any]]]:
        """
        Asynchronously retrieves all rows matching the query criteria.

        This method compiles and executes the query, fetching all resulting
        rows from the database. It returns a list where each element is either
        an instance of the associated model (if one is defined) or a dictionary
        representing a row.

        Use Cases:
        1. Get all records from a table:
           ```python
           users = await query.get_all()
           # Returns a list of all User objects or dictionaries
           ```

        2. Get all records matching a specific condition:
           ```python
           active_users = await query.where(lambda t: t.is_active == True).get_all()
           # Returns a list of all active User objects or dictionaries
           ```

        3. Get all records ordered by a specific column:
           ```python
           products_by_price = await query.order_by(lambda t: t.price).get_all()
           # Returns a list of products ordered by price
           ```

        4. Get a limited number of records:
           ```python
           top_10_users = await query.limit(10).get_all()
           # Returns the first 10 users
           ```

        5. Get records within a specific range (using offset and limit):
           ```python
           paginated_users = await query.offset(20).limit(10).get_all()
           # Returns the users for the third page (if page size is 10)
           ```

        6. Get all unique records:
           ```python
           unique_categories = await query.distinct(lambda t: t.category).get_all()
           # Returns a list of unique category values
           ```

        7. Get all records grouped by a column (often used with aggregation in `select`):
           ```python
           user_counts_by_city = await query.group_by(lambda t: t.city).select(lambda t: [t.city, func.count(t.user_id)]).get_all()
           # Returns a list of (city, user_count) pairs
           ```

        8. Get all records after applying multiple WHERE clauses:
           ```python
           filtered_items = await query.where(lambda t: t.category == 'books').where(lambda t: t.price < 30).get_all()
           # Returns all books with a price under $30
           ```

        9. Get all records ordered by multiple criteria:
           ```python
           sorted_results = await query.order_by(lambda t: t.priority, order_type=OrderType.DESC).then_by(lambda t: t.name).get_all()
           # Returns results sorted by priority (descending) and then by name (ascending)
           ```

        10. Get all records within a specific ID range:
            ```python
            specific_ids = await query.where(lambda t: t.id >= 5).where(lambda t: t.id <= 15).get_all()
            # Returns records with IDs between 5 and 15
            ```

        11. Retrieve all active users sorted by their registration date:
            ```python
            active_users_by_date = await query.where(lambda t: t.is_active == True).order_by(lambda t: t.registration_date).get_all()
            ```

        12. Get all products that belong to a specific category:
            ```python
            category_products = await query.where(lambda t: t.category_id == 123).get_all()
            ```

        13. Retrieve all log entries for a specific user within a date range:
            ```python
            user_logs = await query.where(lambda t: t.user_id == 456).where(lambda t: t.timestamp >= start_date).where(lambda t: t.timestamp <= end_date).order_by(lambda t: t.timestamp).get_all()
            ```

        14. Get all items with a name matching a pattern:
            ```python
            search_results = await query.where(lambda t: t.name.like('%keyword%')).get_all()
            ```

        15. Retrieve all records with a specific boolean flag set to true:
            ```python
            enabled_features = await query.where(lambda t: t.is_enabled == True).get_all()
            ```

        16. Get all records after applying a distinct on a specific field and then ordering:
            ```python
            unique_emails_ordered = await query.distinct(lambda t: t.email).order_by(lambda t: t.email).get_all()
            ```

        17. Retrieve a limited set of the most recent records:
            ```python
            recent_items = await query.order_by(lambda t: t.created_at, order_type=OrderType.DESC).limit(5).get_all()
            ```

        18. Get all records associated with a specific foreign key value:
            ```python
            orders_for_customer = await query.where(lambda t: t.customer_id == 789).get_all()
            ```

        19. Retrieve all records that have a null value in a specific column:
            ```python
            records_with_missing_data = await query.where(lambda t: t.optional_field == None).get_all()
            ```

        20. Get all records after applying a complex filtering and ordering scenario:
            ```python
            complex_results = await query.where(lambda t: (t.status == 'processed') | (t.attempts < 3)).order_by(lambda t: t.priority, order_type=OrderType.DESC).then_by(lambda t: t.completion_time).get_all()
            ```
        """
        self.logger.debug("Entering get_all method.")
        try:
            sql, args = self.compile()
            self.logger.info(f"Executing SQL for get_all(): {sql}, Args: {args}")
            rows = await self.db.fetch(sql, *args)
            result = [
                self.model(**dict(row)) if self._can_return_model() else dict(row)
                for row in rows
            ]
            self.logger.debug(f"'get_all' method retrieved {len(result)} rows.")
            return result
        except ValueError as e:
            self.logger.error(f"Invalid argument in 'get_all' method: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Invalid type in 'get_all' method: {e}")
            raise
        except PostgresError as e:
            self.logger.error(f"Database error during 'get_all': {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error in 'get_all': {e}")
            raise
        finally:
            self.logger.debug("'get_all' method finished.")

    async def get_val(self, column_lambda: Callable[[T], TableField]) -> Any:
        """
        Asynchronously retrieves a single value from a single row.

        This method executes the query, selecting only the specified column and
        limiting the result to one row. It returns the value of that column
        from the first matching row, or `None` if no row is found.

        Use Cases:
        1. Get the name of a specific user:
           ```python
           name = await query.where(lambda t: t.id == 1).get_val(lambda t: t.name)
           # Returns the name of the user with id=1 or None
           ```

        2. Get the email of the first active user:
           ```python
           email = await query.where(lambda t: t.is_active == True).get_val(lambda t: t.email)
           # Returns the email of the first active user or None
           ```

        3. Get the highest price of a product:
           ```python
           max_price = await query.order_by(lambda t: t.price, order_type=OrderType.DESC).get_val(lambda t: t.price)
           # Returns the highest price or None
           ```

        4. Check if a user with a specific username exists (and get their ID):
           ```python
           user_id = await query.where(lambda t: t.username == 'testuser').get_val(lambda t: t.id)
           if user_id:
               print(f"User ID: {user_id}")
           else:
               print("User not found")
           ```

        5. Get the status of a specific item:
           ```python
           status = await query.where(lambda t: t.item_id == 100).get_val(lambda t: t.status)
           # Returns the status of the item or None
           ```

        6. Get a single unique email address:
           ```python
           unique_email = await query.distinct(lambda t: t.email).get_val(lambda t: t.email)
           # Returns one unique email or None
           ```

        7. Get the count of users in a specific city:
           ```python
           user_count = await query.where(lambda t: t.city == 'London').group_by(lambda t: t.city).select(lambda t: func.count(t.user_id)).get_val(lambda t: func.count(t.user_id))
           # Returns the count of users in London or None
           ```

        8. Get the creation timestamp of the first record:
           ```python
           creation_time = await query.order_by(lambda t: t.created_at).get_val(lambda t: t.created_at)
           # Returns the timestamp of the oldest record or None
           ```

        9. Get a single value from a record at a specific offset (e.g., the email of the 5th user):
           ```python
           email_at_offset = await query.offset(4).get_val(lambda t: t.email)
           # Returns the email of the 5th user or None
           ```

        10. Get a single boolean value indicating if a user is active:
            ```python
            is_active = await query.where(lambda t: t.id == 5).get_val(lambda t: t.is_active)
            # Returns True or False if the user exists, otherwise None
            ```

        11. Retrieve a single integer value representing an order quantity:
            ```python
            quantity = await query.where(lambda t: t.order_id == 123).get_val(lambda t: t.quantity)
            ```

        12. Get a single floating-point value representing an average score:
            ```python
            avg_score = await query.get_val(lambda t: func.avg(t.score))
            ```

        13. Retrieve a single string value representing a product description:
            ```python
            description = await query.where(lambda t: t.product_code == 'ABC').get_val(lambda t: t.description)
            ```

        14. Get a single date value representing a registration date:
            ```python
            reg_date = await query.where(lambda t: t.user_id == 789).get_val(lambda t: t.registration_date)
            ```

        15. Retrieve a single value from a record matching multiple criteria:
            ```python
            city = await query.where(lambda t: t.country == 'USA').where(lambda t: t.zip_code == '90210').get_val(lambda t: t.city)
            ```

        16. Get a single value after applying a distinct on one column and filtering on another:
            ```python
            first_unique_status = await query.distinct(lambda t: t.status).where(lambda t: t.category == 'important').get_val(lambda t: t.status)
            ```

        17. Retrieve the minimum value of a certain column:
            ```python
            min_value = await query.get_val(lambda t: func.min(t.value_column))
            ```

        18. Get a single value from the first row of a limited result set after ordering:
            ```python
            top_rated_name = await query.order_by(lambda t: t.rating, order_type=OrderType.DESC).limit(1).get_val(lambda t: t.name)
            ```

        19. Retrieve a single value based on a condition involving a function (e.g., lowercase comparison):
            ```python
            # Assuming lower function is available
            # username = await query.where(lambda t: func.lower(t.email) == 'test@example.com').get_val(lambda t: t.username)
            username = await query.where(lambda t: True).get_val(lambda t: t.username) # Placeholder
            ```

        20. Get a single value from a specific row within a range:
            ```python
            value_in_range = await query.range(2, 3).get_val(lambda t: t.data_value)
            # Gets the data_value from the third row
            ```
        """
        self.logger.debug("Entering get_val method.")
        try:
            if not callable(column_lambda):
                raise TypeError("column_lambda must be a callable")

            self._limit_clause = 1
            table = Table()  # Use the actual table name
            column = column_lambda(table)
            self._select_fields = [column]
            sql, args = self.compile()
            self.logger.info(f"Executing SQL for get_val(): {sql}, Args: {args}")
            result = await self.db.fetchrow(sql, *args)
            if result:
                return result.get(column.name)
            return None
        except ValueError as e:
            self.logger.error(f"Invalid argument in 'get_val' method: {e}")
            raise
        except TypeError as e:
            self.logger.error(f"Invalid type in 'get_val' method: {e}")
            raise
        except PostgresError as e:
            self.logger.error(f"Database error during 'get_val': {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error in 'get_val': {e}")
            raise
        finally:
            self.logger.debug("'get_val' method finished.")

    async def get_column(self, column_lambda: Callable[[T], TableField]) -> List[Any]:
        """
        Asynchronously retrieves all values from a single column for all matching rows.

        This method executes the query, selecting only the specified column. It
        returns a list containing the values of that column from all the rows
        returned by the query.

        Use Cases:
        1. Get a list of all usernames:
           ```python
           usernames = await query.get_column(lambda t: t.username)
           # Returns a list of all usernames
           ```

        2. Get a list of emails for all active users:
           ```python
           active_emails = await query.where(lambda t: t.is_active == True).get_column(lambda t: t.email)
           # Returns a list of emails of active users
           ```

        3. Get a list of prices for all products ordered by price:
           ```python
           prices = await query.order_by(lambda t: t.price).get_column(lambda t: t.price)
           # Returns a sorted list of product prices
           ```

        4. Get the first 10 user IDs:
           ```python
           top_10_ids = await query.limit(10).get_column(lambda t: t.id)
           # Returns a list of the first 10 user IDs
           ```

        5. Get the cities of users on a specific page (using offset and limit):
           ```python
           cities_on_page = await query.offset(20).limit(10).get_column(lambda t: t.city)
           # Returns a list of cities for the users on the third page
           ```

        6. Get a list of all unique email addresses:
           ```python
           unique_emails = await query.distinct(lambda t: t.email).get_column(lambda t: t.email)
           # Returns a list of unique email addresses
           ```

        7. Get a list of counts of users per city:
           ```python
           user_counts = await query.group_by(lambda t: t.city).select(lambda t: func.count(t.user_id)).get_column(lambda t: func.count(t.user_id))
           # Returns a list of user counts for each city
           ```

        8. Get a list of all creation timestamps:
           ```python
           creation_timestamps = await query.get_column(lambda t: t.created_at)
           # Returns a list of all creation timestamps
           ```

        9. Get a list of statuses for items with a specific category:
           ```python
           item_statuses = await query.where(lambda t: t.category == 'electronics').get_column(lambda t: t.status)
           # Returns a list of statuses for electronic items
           ```

        10. Get a list of boolean values indicating if users are premium:
            ```python
            is_premium_list = await query.get_column(lambda t: t.is_premium)
            # Returns a list of True/False values
            ```

        11. Retrieve a list of all order quantities:
            ```python
            quantities = await query.get_column(lambda t: t.quantity)
            ```

        12. Get a list of average scores per group:
            ```python
            avg_scores = await query.group_by(lambda t: t.group_id).select(lambda t: func.avg(t.score)).get_column(lambda t: func.avg(t.score))
            ```

        13. Retrieve a list of all product descriptions:
            ```python
            descriptions = await query.get_column(lambda t: t.description)
            ```

        14. Get a list of all registration dates:
            ```python
            registration_dates = await query.get_column(lambda t: t.registration_date)
            ```

        15. Retrieve a list of cities for users in a specific country:
            ```python
            cities_in_country = await query.where(lambda t: t.country == 'USA').get_column(lambda t: t.city)
            ```

        16. Get a list of unique statuses for a specific item type:
            ```python
            unique_statuses = await query.distinct(lambda t: t.status).where(lambda t: t.item_type == 'widget').get_column(lambda t: t.status)
            ```

        17. Retrieve a list of minimum values for a certain column per group:
            ```python
            min_values = await query.group_by(lambda t: t.group_name).select(lambda t: func.min(t.value_col)).get_column(lambda t: func.min(t.value_col))
            ```

        18. Get a list of names of the top 5 rated items:
            ```python
            top_rated_names = await query.order_by(lambda t: t.rating, order_type=OrderType.DESC).limit(5).get_column(lambda t: t.name)
            ```

        19. Retrieve a list of usernames based on a function (e.g., lowercase):
            ```python
            # Assuming lower function is available
            # lowercase_usernames = await query.get_column(lambda t: func.lower(t.username))
            lowercase_usernames = await query.get_column(lambda t: t.username) # Placeholder
            ```

        20. Get a list of values from a specific column within a defined range of rows:
            ```python
            values_in_range = await query.range(10, 20).get_column(lambda t: t.data_point)
            # Gets the data_point values from rows 11 to 20
            ```
        """
        self.logger.debug("Entering get_column method.")
        try:
            if not callable(column_lambda):
                raise TypeError("column_lambda must be a callable")

            table = Table()
            column = column_lambda(table)
            self._select_fields = [column]
            sql, args = self.compile()
            self.logger.info(f"Executing SQL for get_column(): {sql}, Args: {args}")
            result = await self.db.fetch(sql, *args)
            return [row[column.name] for row in result] if result else []
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'get_column' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'get_column' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'get_column': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'get_column': {e}")
            raise
        finally:
            self.logger.debug("'get_column' method finished.")

    async def get(
        self,
        where_lambda: Optional[Callable[[T], Expression]] = None,
        order_by_lambda: Optional[Callable[[T], TableField]] = None,
        order_type: Optional[OrderType] = None,
        then_by_lambda: Optional[Callable[[T], TableField]] = None,
        then_type: Optional[OrderType] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        distinct: bool = False,
        distinct_on_lambda: Optional[Callable[[T], TableField]] = None,
        columns_lambda: Optional[
            Callable[[T], List[Union[TableField, str, Function]]]
        ] = None,
    ) -> Union[List[T], List[Dict[str, Any]]]:
        """
        Asynchronously retrieves multiple rows from the database with various options.

        This method provides a flexible way to fetch data based on specified
        conditions, ordering, limiting, offsetting, and distinctness. It combines
        the functionality of several other methods into one for convenience.

        Use Cases:
        1. Get all users:
           ```python
           users = await query.get()
           ```

        2. Get active users:
           ```python
           active_users = await query.get(where_lambda=lambda t: t.is_active == True)
           ```

        3. Get users ordered by name:
           ```python
           users_by_name = await query.get(order_by_lambda=lambda t: t.name)
           ```

        4. Get the top 10 users by registration date (descending):
           ```python
           top_users = await query.get(order_by_lambda=lambda t: t.registration_date, order_type=OrderType.DESC, limit=10)
           ```

        5. Get users on the second page (page size 15):
           ```python
           page_two_users = await query.get(limit=15, offset=15)
           ```

        6. Get all unique email addresses:
           ```python
           unique_emails = await query.get(distinct=True, columns_lambda=lambda t: [t.email])
           ```

        7. Get the first unique user per city:
           ```python
           first_user_per_city = await query.get(distinct_on_lambda=lambda t: t.city, order_by_lambda=lambda t: t.city)
           ```

        8. Get specific columns for all users:
           ```python
           user_details = await query.get(columns_lambda=lambda t: [t.id, t.username])
           ```

        9. Get inactive users ordered by their last login date (ascending), then by username:
           ```python
           inactive_users = await query.get(where_lambda=lambda t: t.is_active == False, order_by_lambda=lambda t: t.last_login, then_by_lambda=lambda t: t.username)
           ```

        10. Get a limited number of records with a complex filter:
            ```python
            filtered_results = await query.get(where_lambda=lambda t: (t.status == 'processed') & (t.attempts < 5), limit=50)
            ```

        11. Get all records ordered by a foreign key:
            ```python
            orders_by_customer = await query.get(order_by_lambda=lambda t: t.customer_id)
            ```

        12. Get records with a specific value in a boolean column:
            ```python
            premium_users = await query.get(where_lambda=lambda t: t.is_premium == True)
            ```

        13. Get records within a specific range of IDs, ordered by creation date:
            ```python
            id_range_records = await query.get(where_lambda=lambda t: (t.id >= 100) & (t.id <= 200), order_by_lambda=lambda t: t.created_at)
            ```

        14. Get the first record matching a complex set of criteria:
            ```python
            first_match = await query.get(where_lambda=lambda t: (t.category == 'A') | ((t.category == 'B') & (t.priority > 3)), limit=1)
            ```

        15. Get distinct values of a column ordered descending:
            ```python
            distinct_values_desc = await query.get(distinct=True, columns_lambda=lambda t: [t.value_column], order_by_lambda=lambda t: t.value_column, order_type=OrderType.DESC)
            ```

        16. Get a specific set of columns with a limit and offset:
            ```python
            partial_data = await query.get(columns_lambda=lambda t: [t.field1, t.field2], limit=25, offset=50)
            ```

        17. Get records ordered by one column ascending and then another descending:
            ```python
            double_ordered = await query.get(order_by_lambda=lambda t: t.group, then_by_lambda=lambda t: t.sort_order, then_type=OrderType.DESC)
            ```

        18. Get distinct records based on multiple columns:
            ```python
            unique_combinations = await query.get(distinct=True, columns_lambda=lambda t: [t.col1, t.col2])
            ```

        19. Get records filtered by a range of dates:
            ```python
            date_range_data = await query.get(where_lambda=lambda t: (t.event_date >= start_date) & (t.event_date <= end_date))
            ```

        20. Get a small sample of records ordered randomly (if your database supports random ordering):
            ```python
            # Assuming a way to express random ordering in your ORM
            # random_sample = await query.get(order_by_lambda=lambda t: func.random(), limit=5)
            random_sample = await query.get(limit=5) # Placeholder for random ordering
            ```
        """
        self.logger.debug("Entering get method.")
        try:
            if where_lambda is not None and not callable(where_lambda):
                raise TypeError("where_lambda must be a callable")

            if order_by_lambda is not None and not callable(order_by_lambda):
                raise TypeError("order_by_lambda must be a callable")

            if then_by_lambda is not None and not callable(then_by_lambda):
                raise TypeError("then_by_lambda must be a callable")

            if distinct_on_lambda is not None and not callable(distinct_on_lambda):
                raise TypeError("distinct_on_lambda must be a callable")

            if columns_lambda is not None and not callable(columns_lambda):
                raise TypeError("columns_lambda must be a callable")

            if columns_lambda:
                self.select(columns_lambda)
            elif not self._select_fields:
                pass  # Select all fields if no select has been made

            if where_lambda:
                self.where(where_lambda)
            if order_by_lambda:
                self.order_by(order_by_lambda, order_type)
                if then_by_lambda:
                    self.then_by(then_by_lambda, then_type)
            if limit is not None:
                self.limit(limit)
            if offset is not None:
                self.offset(offset)
            if distinct:
                if distinct_on_lambda:
                    self.distinct(distinct_on_lambda)
                else:
                    self.distinct()

            sql, args = self.compile()
            self.logger.debug(f"Executing get query: {sql}, Args: {args}")

            try:
                rows = await self.db.fetch(sql, *args)
            except ValueError as e:
                self.logger.exception(f"Invalid argument in 'get' method: {e}")
                raise
            except Exception as e:
                self.logger.exception(f"Database error during 'get': {e}")
                raise
            finally:
                self.logger.debug("Finished 'get' method execution.")

            return (
                [self.model(**dict(row)) for row in rows]
                if self._can_return_model()
                else [dict(row) for row in rows]
            )
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'get' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'get' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'get': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'get': {e}")
            raise
        finally:
            self.logger.debug("'get' method finished.")

    async def get_by_id(self, id_val: Any, id_field: str = "id") -> Optional[T]:
        """
        Asynchronously retrieves a single record by its unique identifier.

        This method is a convenient way to fetch a record based on its ID.
        It defaults to looking for a column named "id", but you can specify
        a different column name using the `id_field` parameter. It returns
        the model instance or a dictionary if found, otherwise `None`.

        Use Cases:
        1. Get a user by their ID (assuming the ID column is named 'id'):
           ```python
           user = await query.get_by_id(123)
           # Returns the User object with ID 123 or None
           ```

        2. Get a product by its product code:
           ```python
           product = await query.get_by_id("ABC-123", id_field="product_code")
           # Returns the Product object with product code 'ABC-123' or None
           ```

        3. Get an order by its order number:
           ```python
           order = await query.get_by_id(1001, id_field="order_number")
           # Returns the Order object with order number 1001 or None
           ```

        4. Attempt to get a non-existent user by ID:
           ```python
           non_existent_user = await query.get_by_id(9999)
           # Returns None
           ```

        5. Get a record using a composite primary key (if your model represents it):
           ```python
           # Assuming a model with composite key (user_id, session_id)
           # You might need to adjust how the where clause is constructed
           # composite_key = {"user_id": 456, "session_id": "xyz"}
           # session = await query.where(lambda t: (t.user_id == composite_key['user_id']) & (t.session_id == composite_key['session_id'])).get_one()
           session = await query.where(lambda t: True).get_one() # Placeholder
           ```

        6. Get a log entry by its unique log ID:
           ```python
           log = await query.get_by_id(50, id_field="log_id")
           # Returns the LogEntry object with log_id 50 or None
           ```

        7. Get a configuration setting by its key:
           ```python
           config = await query.get_by_id("max_retries", id_field="key")
           # Returns the Configuration object with key 'max_retries' or None
           ```

        8. Get a record where the ID is not an integer:
           ```python
           item = await query.get_by_id("unique-string-id", id_field="uuid")
           # Returns the Item object with the given UUID or None
           ```

        9. Handle cases where the specified ID field does not exist in the model:
           ```python
           try:
               invalid = await query.get_by_id(1, id_field="non_existent_field")
           except ValueError as e:
               print(f"Error: {e}")
           ```

        10. Get a record based on a foreign key that acts as a unique identifier in that context:
            ```python
            # Assuming 'profile_id' is unique for Profile records
            profile = await query.get_by_id(789, id_field="profile_id")
            # Returns the Profile object with profile_id 789 or None
            ```

        11. Retrieve a single record based on an indexed column that serves as a unique identifier:
            ```python
            unique_code_record = await query.get_by_id("special-code", id_field="unique_code")
            ```

        12. Get a record using an ID value that might be of a different type (handled by the underlying database driver):
            ```python
            # Assuming the database can handle the type conversion if needed
            record = await query.get_by_id("123", id_field="numeric_id")
            ```

        13. Attempt to retrieve a record with a null ID value (if allowed by the database schema):
            ```python
            null_id_record = await query.get_by_id(None)
            # Behavior depends on how null IDs are handled
            ```

        14. Get a record using a case-sensitive ID (if the database is case-sensitive):
            ```python
            case_sensitive_record = await query.get_by_id("CaseSensitiveID", id_field="case_sensitive_id")
            ```

        15. Retrieve a record where the ID is a date or timestamp:
            ```python
            import datetime
            specific_event = await query.get_by_id(datetime.date(2023, 1, 15), id_field="event_date")
            ```

        16. Get a record using an ID that is part of a JSON structure (if your database supports JSON querying):
            ```python
            # Assuming JSON querying capabilities
            # json_id_record = await query.where(lambda t: t.json_data['id'] == 42).get_one()
            json_id_record = await query.where(lambda t: True).get_one() # Placeholder
            ```

        17. Retrieve a record by an ID that has leading/trailing whitespace (assuming exact match is needed):
            ```python
            whitespace_id_record = await query.get_by_id("  ID 1  ", id_field="spaced_id")
            ```

        18. Get a record where the ID is a serialized value (e.g., a string representation of a list or dictionary):
            ```python
            # Assuming the ID is stored as a string
            serialized_id_record = await query.get_by_id("[1, 2, 3]", id_field="serialized_id")
            ```

        19. Retrieve a record by an ID that is auto-incrementing (the typical use case):
            ```python
            auto_increment_record = await query.get_by_id(101)
            ```

        20. Get a record using an ID from a different table (if IDs are globally unique or contextually unique):
            ```python
            # Assuming a globally unique ID across tables
            cross_table_record = await query.get_by_id("some-global-id", id_field="global_id")
            ```
        """
        self.logger.debug("Entering get_by_id method.")
        try:
            table = Table()
            if not hasattr(table, id_field):
                raise ValueError(
                    f"The object '{table.__class__.__name__}' does not have an attribute named '{id_field}'."
                )
            where_expression = getattr(table, id_field) == id_val
            result = await self.where(lambda t: where_expression).get_one()
            return result
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'get_by_id' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'get_by_id' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'get_by_id': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'get_by_id': {e}")
            raise
        finally:
            self.logger.debug("'get_by_id' method finished.")

    async def get_pages(
        self,
        where_lambda: Optional[Callable[[T], Expression]] = None,
        order_by_lambda: Optional[Callable[[T], TableField]] = None,
        order_type: OrderType = OrderType.ASC,
        then_by_lambda: Optional[Callable[[T], TableField]] = None,
        then_type: OrderType = OrderType.ASC,
        page: int = 1,
        page_size: int = 10,
        distinct: bool = False,
        distinct_on_lambda: Optional[Callable[[T], TableField]] = None,
        columns_lambda: Optional[
            Callable[[T], List[Union[TableField, str, Function]]]
        ] = None,
    ) -> "PagedResults[T]":
        """
        Asynchronously retrieves results in paginated form.

        This method fetches a specific page of results based on the provided
        parameters, including filtering, ordering, and pagination settings.
        It also returns the total number of matching items, allowing for
        easy implementation of pagination controls.

        Use Cases:
        1. Get the first page of users (default page size 10):
           ```python
           paged_users = await query.get_pages()
           # Returns a PagedResults object containing the first 10 users
           ```

        2. Get the third page of products with a page size of 20:
           ```python
           page_three_products = await query.get_pages(page=3, page_size=20)
           # Returns the 41st to 60th products
           ```

        3. Get the first page of active users ordered by name:
           ```python
           active_users_page_one = await query.get_pages(where_lambda=lambda t: t.is_active == True, order_by_lambda=lambda t: t.name)
           ```

        4. Get the second page of orders ordered by date (descending):
           ```python
           page_two_orders = await query.get_pages(page=2, page_size=15, order_by_lambda=lambda t: t.order_date, order_type=OrderType.DESC)
           ```

        5. Get the first page of unique email addresses:
           ```python
           unique_emails_paged = await query.get_pages(distinct=True, columns_lambda=lambda t: [t.email])
           ```

        6. Get the first page of distinct users per city (ordered by city):
           ```python
           first_user_per_city_paged = await query.get_pages(distinct_on_lambda=lambda t: t.city, order_by_lambda=lambda t: t.city)
           ```

        7. Get the first page with specific columns:
           ```python
           partial_users_page_one = await query.get_pages(columns_lambda=lambda t: [t.id, t.username])
           ```

        8. Get a specific page with secondary ordering:
           ```python
           paged_results = await query.get_pages(page=2, order_by_lambda=lambda t: t.group, then_by_lambda=lambda t: t.sort_order)
           ```

        9. Get the first page of results matching a complex filter:
           ```python
           filtered_page_one = await query.get_pages(where_lambda=lambda t: (t.status == 'pending') | (t.priority > 3))
           ```

        10. Get the last page of results (you might need to calculate the total pages):
            ```python
            paged_results = await query.get_pages(page=total_pages, page_size=25)
            ```

        11. Retrieve the first page of records ordered by a foreign key:
            ```python
            paged_orders = await query.get_pages(order_by_lambda=lambda t: t.customer_id)
            ```

        12. Get the first page of records with a specific boolean flag:
            ```python
            paged_premium_users = await query.get_pages(where_lambda=lambda t: t.is_premium == True)
            ```

        13. Retrieve a specific page within a range of IDs:
            ```python
            paged_ids = await query.get_pages(where_lambda=lambda t: (t.id >= 50) & (t.id <= 150), page=2, page_size=10)
            ```

        14. Get the first page of distinct combinations of two columns:
            ```python
            paged_unique_combinations = await query.get_pages(distinct=True, columns_lambda=lambda t: [t.col1, t.col2])
            ```

        15. Retrieve the first page of records filtered by a date range:
            ```python
            paged_dates = await query.get_pages(where_lambda=lambda t: (t.event_date >= start_date) & (t.event_date <= end_date))
            ```

        16. Get the first page ordered descending:
            ```python
            desc_paged = await query.get_pages(order_by_lambda=lambda t: t.value, order_type=OrderType.DESC)
            ```

        17. Retrieve a specific page with a different ordering for the secondary sort:
            ```python
            alt_secondary_sort = await query.get_pages(page=1, order_by_lambda=lambda t: t.main_field, then_by_lambda=lambda t: t.secondary_field, then_type=OrderType.DESC)
            ```

        18. Get the first page of distinct records based on a function's output:
            ```python
            # Assuming a function is used in distinct_on_lambda
            # paged_distinct_func = await query.get_pages(distinct_on_lambda=lambda t: func.lower(t.email))
            paged_distinct_func = await query.get_pages() # Placeholder
            ```

        19. Retrieve a specific page with no ordering specified:
            ```python
            unordered_page = await query.get_pages(page=4, page_size=5)
            ```

        20. Get the first page with a very large page size (effectively getting all or a large chunk):
            ```python
            large_page = await query.get_pages(page_size=1000)
            ```
        """
        self.logger.debug("Entering get_pages method.")
        try:
            if where_lambda is not None and not callable(where_lambda):
                raise TypeError("where_lambda must be a callable")

            if order_by_lambda is not None and not callable(order_by_lambda):
                raise TypeError("order_by_lambda must be a callable")

            if then_by_lambda is not None and not callable(then_by_lambda):
                raise TypeError("then_by_lambda must be a callable")

            if distinct_on_lambda is not None and not callable(distinct_on_lambda):
                raise TypeError("distinct_on_lambda must be a callable")

            if columns_lambda is not None and not callable(columns_lambda):
                raise TypeError("columns_lambda must be a callable")

            if page < 1 or page_size <= 0:
                raise ValueError("Invalid page or page_size")

            # Count total items
            count_query = Query[T](self.table_name, self.model, self.db, self.logger)
            if where_lambda:
                count_query.where(where_lambda)

            total_count_result = await count_query.select(
                lambda t: [Table().count(alias="count")]
            ).get_one()
            total_count = (
                total_count_result.get("count", 0) if total_count_result else 0
            )

            # Fetch items for the current page
            offset = (page - 1) * page_size
            items_query = self
            if where_lambda:
                items_query = items_query.where(where_lambda)
            if columns_lambda:
                items_query = items_query.select(columns_lambda)
            if order_by_lambda:
                items_query = items_query.order_by(order_by_lambda, order_type)
                if then_by_lambda:
                    items_query = items_query.then_by(then_by_lambda, then_type)
            if distinct:
                if distinct_on_lambda:
                    items_query = items_query.distinct(distinct_on_lambda)
                else:
                    items_query.distinct()

            items = await items_query.limit(page_size).offset(offset).get_all()
            return PagedResults[T](
                items=items,
                total_count=total_count,
                page_number=page,
                page_size=page_size,
            )
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'get_pages' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'get_pages' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'get_pages': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'get_pages': {e}")
            raise
        finally:
            self.logger.debug("'get_pages' method finished.")

    async def create(
        self,
        data: T,
        returning_fields_lambda: Optional[
            Callable[[T], List[Union[TableField, str]]]
        ] = None,
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Asynchronously creates a new record in the database.

        This method takes a data object (either a model instance or a dictionary),
        extracts its values, and inserts a new row into the associated table.
        It can optionally return specific fields of the newly created record.

        Use Cases:
        1. Create a new user and return the newly created user object:
           ```python
           new_user = User(name="John Doe", email="john.doe@example.com")
           created_user = await query.create(new_user)
           # Returns the newly created User object with its ID
           ```

        2. Create a new product and return its ID:
           ```python
           new_product = {"name": "Laptop", "price": 1200}
           created_product_id = await query.create(new_product, returning_fields_lambda=lambda t: [t.id])
           # Returns a dictionary like {'id': 456}
           ```

        3. Create a log entry with a timestamp:
           ```python
           import datetime
           new_log = {"message": "User logged in", "created_at": datetime.datetime.now()}
           created_log = await query.create(new_log)
           # Returns the newly created log entry
           ```

        4. Create multiple records (this method creates one at a time; for bulk insert, a separate method might be needed):
           ```python
           users_to_create = [User(name="Jane Doe", email="jane.doe@example.com"), User(name="Peter Pan", email="peter.pan@neverland.com")]
           created_users = [await query.create(user) for user in users_to_create]
           ```

        5. Create a record and return multiple fields:
           ```python
           new_item = {"name": "Book", "author": "Unknown", "price": 20}
           created_item_details = await query.create(new_item, returning_fields_lambda=lambda t: [t.id, t.name, t.price])
           # Returns a dictionary with id, name, and price
           ```

        6. Create a record where the ID is auto-generated and return the full record:
           ```python
           new_category = {"name": "Fiction"}
           created_category = await query.create(new_category)
           # Returns the created category with its auto-generated ID
           ```

        7. Create a record without specifying a returning clause (will return all fields by default):
           ```python
           new_setting = {"key": "theme", "value": "dark"}
           created_setting = await query.create(new_setting)
           ```

        8. Attempt to create a record with missing required fields (database error might occur):
           ```python
           incomplete_data = {"name": "Test"}
           try:
               await query.create(incomplete_data)
           except PostgresError as e:
               print(f"Database error: {e}")
           ```

        9. Create a record with a null value for a nullable field:
           ```python
           optional_data = {"name": "Optional", "description": None}
           created_optional = await query.create(optional_data)
           ```

        10. Create a record with a value for a field with a default database value (the default might be used if not provided):
            ```python
            # Assuming 'is_active' has a default of False in the database
            new_task = {"title": "Review pending tasks"}
            created_task = await query.create(new_task)
            # 'is_active' will likely be False
            ```

        11. Create a record and return a field with a database-generated value (e.g., timestamp):
            ```python
            new_event = {"name": "User registered"}
            created_event = await query.create(new_event, returning_fields_lambda=lambda t: [t.event_time])
            # Returns the database-generated event_time
            ```

        12. Create a record with specific data types:
            ```python
            import datetime
            data_types = {"int_col": 123, "float_col": 3.14, "bool_col": True, "date_col": datetime.date(2025, 5, 20)}
            created_typed_data = await query.create(data_types)
            ```

        13. Create a record where a field is a foreign key:
            ```python
            new_post = {"title": "My Post", "user_id": 1}
            created_post = await query.create(new_post)
            ```

        14. Create a record and return a calculated or transformed value (if supported by the database's RETURNING clause):
            ```python
            # Example assuming a database function 'UPPER' exists
            # created_upper_name = await query.create({"name": "lowercase"}, returning_fields_lambda=lambda t: [func.upper(t.name)])
            created_upper_name = await query.create({"name": "lowercase"}, returning_fields_lambda=lambda t: [t.name]) # Placeholder
            ```

        15. Create a record with JSON data:
            ```python
            json_data = {"config": {"theme": "light", "font_size": 12}}
            created_json = await query.create(json_data)
            ```

        16. Create a record with array data:
            ```python
            array_data = {"tags": ["python", "asyncio"]}
            created_array = await query.create(array_data)
            ```

        17. Create a record and only return the primary key ID as an integer:
            ```python
            new_entity = {"value": "some value"}
            created_id = await query.create(new_entity, returning_fields_lambda=lambda t: [t.id])
            # Returns {'id': 789}
            ```

        18. Attempt to create a record with a unique constraint violation (database error will occur):
            ```python
            try:
                await query.create({"unique_field": "existing_value"})
            except PostgresError as e:
                print(f"Unique constraint violation: {e}")
            ```

        19. Create a record with a default timestamp value (if 'created_at' is not provided):
            ```python
            simple_record = {"data": "some data"}
            created_simple = await query.create(simple_record)
            # 'created_at' will be auto-filled if the logic is in the method
            ```

        20. Create a record and return a specific field aliased with a different name:
            ```python
            created_alias = await query.create({"original_name": "value"}, returning_fields_lambda=lambda t: [t.original_name.label("newName")])
            # Returns {'newName': 'value'}
            ```
        """
        self.logger.debug("Entering create method.")
        try:
            if returning_fields_lambda is not None and not callable(
                returning_fields_lambda
            ):
                raise TypeError("returning_fields_lambda must be a callable")

            if not data:
                raise ValueError("`data` object cannot be None for create operation")

            columns = list(data.__dict__.keys())

            # Auto-fill 'created_at'
            if (
                hasattr(data, "created_at")
                and getattr(data, "created_at", None) is None
            ):
                now = datetime.datetime.now(pytz.utc)
                setattr(data, "created_at", now)
                if "created_at" not in columns:
                    columns.append("created_at")

            insert_columns = []
            insert_values = []
            for col in columns:
                value = getattr(data, col)
                if col == "id" and value is None:
                    continue  # Skip id for SERIAL columns
                insert_columns.append(col)
                insert_values.append(value)

            placeholders = ", ".join(f"${i + 1}" for i in range(len(insert_columns)))
            sql = f"INSERT INTO {self.table_name} ({', '.join(insert_columns)}) VALUES ({placeholders})"

            returning_fields = None
            if returning_fields_lambda:
                table = Table()
                returning_fields = returning_fields_lambda(table)

            if returning_fields:
                returning_clause = f" RETURNING {', '.join(compile_expression(field, []) for field in returning_fields)}"
                sql += returning_clause
                self.logger.info(
                    f"Executing CREATE SQL with returning fields: {sql}, Args: {insert_values}"
                )
                row = await self.db.fetchrow(sql, *insert_values)
                return dict(row) if row else None
            else:
                sql += " RETURNING *"
                self.logger.info(
                    f"Executing CREATE SQL with default returning: {sql}, Args: {insert_values}"
                )
                row = await self.db.fetchrow(sql, *insert_values)
                if row and self._can_return_model():
                    return self.model(**dict(row))
                elif row:
                    return dict(row)
                return None
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'create' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'create' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'create': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'create': {e}")
            raise
        finally:
            self.logger.debug("'create' method finished.")

    async def bulk_create(self, data_list: List[T]) -> int:
        """
        Efficiently inserts multiple records into the database.

        This method takes a list of data objects (model instances) and performs
        a single database operation to insert them, which is more performant
        than creating records one by one. All objects in the list must have
        the same set of fields. It returns the number of rows inserted.

        Use Cases:
        1. Insert a list of new users:
           ```python
           new_users = [User(name="Alice", email="alice@example.com"), User(name="Bob", email="bob@example.com")]
           inserted_count = await query.bulk_create(new_users)
           # Returns 2
           ```

        2. Add multiple products at once:
           ```python
           new_products = [{"name": "Mouse", "price": 25}, {"name": "Keyboard", "price": 75}]
           inserted = await query.bulk_create([Product(**p) for p in new_products])
           # Returns 2
           ```

        3. Log multiple events:
           ```python
           import datetime
           now = datetime.datetime.now(pytz.utc)
           new_logs = [Log(message="User A logged in", created_at=now), Log(message="User B logged out", created_at=now)]
           count = await query.bulk_create(new_logs)
           # Returns 2
           ```

        4. Seed initial data into a table:
           ```python
           initial_configs = [Config(key="max_attempts", value=5), Config(key="retry_interval", value=30)]
           inserted = await query.bulk_create(initial_configs)
           ```

        5. Import data from an external source in bulk:
           ```python
           imported_data = [DataItem(field1=val1, field2=val2) for _ in range(100)]
           inserted_rows = await query.bulk_create(imported_data)
           # Returns 100
           ```

        6. Create multiple related entities (e.g., multiple order items for a single order):
           ```python
           order_items = [OrderItem(order_id=1, product_id=101, quantity=2), OrderItem(order_id=1, product_id=102, quantity=1)]
           created_items_count = await query.bulk_create(order_items)
           # Returns 2
           ```

        7. Batch insert sensor readings:
           ```python
           sensor_data = [SensorReading(sensor_id=1, value=22.5, timestamp=now), SensorReading(sensor_id=2, value=15.8, timestamp=now)]
           inserted = await query.bulk_create(sensor_data)
           ```

        8. Create multiple user roles:
           ```python
           new_roles = [Role(name="admin"), Role(name="editor"), Role(name="viewer")]
           inserted_roles = await query.bulk_create(new_roles)
           # Returns 3
           ```

        9. Insert a list of records with auto-generated IDs (the ID column will be skipped if None in the first item):
           ```python
           new_entries = [Entry(title="Entry 1", content="..."), Entry(title="Entry 2", content="...")]
           inserted_count = await query.bulk_create(new_entries)
           ```

        10. Bulk insert where 'created_at' should be automatically set:
            ```python
            new_events = [Event(type="login"), Event(type="logout")]
            inserted = await query.bulk_create(new_events)
            # 'created_at' will be set to the current time for both
            ```

        11. Insert a large number of records efficiently:
            ```python
            large_dataset = [DataRecord(field_a=i, field_b=str(i)) for i in range(1000)]
            inserted = await query.bulk_create(large_dataset)
            # Returns 1000
            ```

        12. Create multiple records with different but consistent data types:
            ```python
            data_points = [Point(x=1, y=2.5), Point(x=3, y=4.7)]
            inserted = await query.bulk_create(data_points)
            ```

        13. Bulk create records with foreign key relationships:
            ```python
            new_comments = [Comment(post_id=10, text="Comment 1"), Comment(post_id=10, text="Comment 2")]
            inserted = await query.bulk_create(new_comments)
            ```

        14. Insert a list of records without explicitly setting a primary key (assuming auto-increment):
            ```python
            new_tasks = [Task(description="Task A"), Task(description="Task B")]
            inserted = await query.bulk_create(new_tasks)
            ```

        15. Bulk insert records with some fields having default database values:
            ```python
            # Assuming 'status' has a default value
            new_jobs = [Job(name="Job X"), Job(name="Job Y")]
            inserted = await query.bulk_create(new_jobs)
            ```

        16. Insert multiple records with identical data:
            ```python
            default_settings = [DefaultSetting(key="option1", value="default"), DefaultSetting(key="option2", value="default")]
            inserted = await query.bulk_create(default_settings)
            ```

        17. Bulk create records where one of the fields is a JSON object:
            ```python
            configs = [AppConfig(settings={"theme": "dark"}), AppConfig(settings={"notifications": True})]
            inserted = await query.bulk_create(configs)
            ```

        18. Insert a list of records with array data:
            ```python
            new_docs = [Document(tags=["a", "b"]), Document(tags=["c", "d", "e"])]
            inserted = await query.bulk_create(new_docs)
            ```

        19. Attempt to bulk insert an empty list (should raise ValueError):
            ```python
            try:
                await query.bulk_create([])
            except ValueError as e:
                print(f"Error: {e}")
            ```

        20. Bulk insert records with a mix of provided and auto-generated timestamps:
            ```python
            import datetime
            now = datetime.datetime.now(pytz.utc)
            mixed_times = [EventLog(action="start", timestamp=now), EventLog(action="end")]
            inserted = await query.bulk_create(mixed_times)
            # The second one's timestamp will be auto-generated
            ```
        """
        self.logger.debug("Entering bulk_create method.")
        try:
            if not data_list:
                raise ValueError(
                    "`data_list` cannot be empty for bulk_create operation"
                )

            first_item = data_list[0]
            columns = [
                c for c in list(first_item.__dict__.keys()) if not c.startswith("_")
            ]

            # Check 'id' field. Remove if None in the first element (for SERIAL).
            if "id" in columns and getattr(first_item, "id", None) is None:
                columns.remove("id")

            # Auto-fill 'created_at'
            if hasattr(first_item, "created_at") and "created_at" in columns:
                pass  # Values will be added later
            elif hasattr(first_item, "created_at") and "created_at" not in columns:
                columns.append("created_at")

            num_columns = len(columns)
            placeholders = ", ".join(
                f"({', '.join(f'${i + 1 + j * num_columns}' for i in range(num_columns))})"
                for j in range(len(data_list))
            )

            values = []
            for item in data_list:
                item_values = []
                for col in columns:
                    if col == "created_at":
                        if (
                            hasattr(item, "created_at")
                            and getattr(item, "created_at", None) is not None
                        ):
                            item_values.append(getattr(item, "created_at"))
                        else:
                            item_values.append(datetime.datetime.now(pytz.utc))
                        continue
                    item_values.append(getattr(item, col))
                values.extend(item_values)

            sql = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES {placeholders}"

            self.logger.info(f"Executing BULK CREATE SQL: {sql}, Args: {values}")
            try:
                await self.db.execute(sql, *values)
                return len(data_list)
            except Exception as e:
                self.logger.error(f"Error executing BULK CREATE SQL: {e}")
                return 0
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'bulk_create' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'bulk_create' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'bulk_create': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'bulk_create': {e}")
            raise
        finally:
            self.logger.debug("'bulk_create' method finished.")

    async def update(
        self,
        data: dict,
        where_lambda: Optional[Callable[[T], Expression]] = None,
        returning_fields_lambda: Optional[
            Callable[[T], List[Union[TableField, str]]]
        ] = None,
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Asynchronously updates records in the database based on a condition.

        This method takes a dictionary of data to update and an optional
        `where_lambda` to specify which records should be updated. It's crucial
        to provide a `where_lambda` to avoid updating the entire table.
        It can optionally return specific fields of the updated record(s).

        Use Cases:
        1. Update a user's email by their ID and return the updated user:
           ```python
           updated_user = await query.where(lambda t: t.id == 123).update({"email": "new.email@example.com"})
           # Returns the updated User object or None
           ```

        2. Update multiple active users' status to 'processed':
           ```python
           updated_count = await query.where(lambda t: t.is_active == True).update({"status": "processed"})
           # Returns None by default if returning_fields_lambda is not used
           ```

        3. Update a product's price and return its new price:
           ```python
           new_price = await query.where(lambda t: t.product_code == "XYZ").update({"price": 99.99}, returning_fields_lambda=lambda t: [t.price])
           # Returns a dictionary like {'price': 99.99}
           ```

        4. Update a record using multiple conditions in the WHERE clause:
           ```python
           updated_item = await query.where(lambda t: (t.category == 'A') & (t.priority > 5)).update({"status": "high_priority"})
           ```

        5. Update a record and return multiple fields:
           ```python
           updated_details = await query.where(lambda t: t.order_id == 101).update({"status": "shipped", "shipped_at": datetime.datetime.now()}, returning_fields_lambda=lambda t: [t.status, t.shipped_at])
           # Returns a dictionary with status and shipped_at
           ```

        6. Update a record by a non-ID field:
           ```python
           updated_profile = await query.where(lambda t: t.username == "johndoe").update({"bio": "Updated bio"})
           ```

        7. Update a record and return the original values before the update (if supported by the database):
           ```python
           # Some databases might have specific syntax for this
           # original_values = await query.where(lambda t: t.id == 5).update({"counter": t.counter + 1}, returning_fields_lambda=lambda t: [t.counter])
           original_values = await query.where(lambda t: t.id == 5).update({"counter": 1}, returning_fields_lambda=lambda t: [t.counter]) # Placeholder
           ```

        8. Update a JSON field within a record (if the database supports JSON functions):
           ```python
           # Example assuming a database function to update JSON
           # updated_config = await query.where(lambda t: t.key == "settings").update({"config": func.jsonb_set(t.config, '{theme}', '"dark"'::jsonb)})
           updated_config = await query.where(lambda t: t.key == "settings").update({"config": {"theme": "dark"}}) # Placeholder
           ```

        9. Update an array field (if the database supports array functions):
           ```python
           # Example assuming a database function to append to an array
           # updated_tags = await query.where(lambda t: t.doc_id == 1).update({"tags": func.array_append(t.tags, 'new_tag')})
           updated_tags = await query.where(lambda t: t.doc_id == 1).update({"tags": ["old_tag", "new_tag"]}) # Placeholder
           ```

        10. Update a record and return a calculated value after the update:
            ```python
            updated_total = await query.where(lambda t: t.item_id == 200).update({"quantity": t.quantity + 1}, returning_fields_lambda=lambda t: [t.quantity * t.unit_price])
            ```

        11. Update multiple records based on a date range:
            ```python
            updated_events = await query.where(lambda t: (t.event_date >= start_date) & (t.event_date <= end_date)).update({"status": "completed"})
            ```

        12. Update records where a field is NULL:
            ```python
            updated_records = await query.where(lambda t: t.notes == None).update({"notes": "No notes provided"})
            ```

        13. Update records and return a boolean flag indicating success (if the database's fetchrow returns something):
            ```python
            update_result = await query.where(lambda t: t.login_attempts >= 3).update({"is_locked": True}, returning_fields_lambda=lambda t: [True])
            # Might return a dictionary like {'True': True}
            ```

        14. Attempt an update without a WHERE clause (should raise ValueError):
            ```python
            try:
                await query.update({"status": "inactive"})
            except ValueError as e:
                print(f"Error: {e}")
            ```

        15. Update a record using a subquery in the WHERE clause (if supported by your ORM):
            ```python
            # Example of a conceptual subquery
            # await query.where(lambda t: t.user_id.in_(select(...).where(...))).update({"is_premium": True})
            await query.where(lambda t: True).update({"is_premium": True}) # Placeholder
            ```

        16. Update a record and return a transformed value:
            ```python
            updated_name = await query.where(lambda t: t.id == 7).update({"name": "old name"}, returning_fields_lambda=lambda t: [func.upper(t.name)])
            # Returns the uppercase version of the name
            ```

        17. Update records based on a LIKE condition:
            ```python
            updated_items = await query.where(lambda t: t.description.like('%special%')).update({"discount": 0.1})
            ```

        18. Update records with values derived from existing columns:
            ```python
            updated_inventory = await query.update({"stock_level": t.stock_level - 1}, where_lambda=lambda t: t.product_id == 50)
            ```

        19. Update a record and return a specific field with an alias:
            ```python
            updated_alias = await query.where(lambda t: t.id == 9).update({"value": 100}, returning_fields_lambda=lambda t: [t.value.label("newValue")])
            # Returns {'newValue': 100}
            ```

        20. Update multiple records with different values based on a condition (you might need multiple update calls or a more complex query depending on the logic):
            ```python
            await query.where(lambda t: t.group == 'A').update({"priority": 1})
            await query.where(lambda t: t.group == 'B').update({"priority": 2})
            ```
        """
        self.logger.debug("Entering update method.")
        try:
            if where_lambda is not None and not callable(where_lambda):
                raise TypeError("where_lambda must be a callable")

            if returning_fields_lambda is not None and not callable(
                returning_fields_lambda
            ):
                raise TypeError("returning_fields_lambda must be a callable")

            if not data:
                raise ValueError(
                    "`data` dictionary cannot be empty for update operation"
                )

            update_data = data.copy()
            # Add current time to 'updated_at' if the key exists
            if "updated_at" in update_data:
                update_data["updated_at"] = datetime.datetime.now(pytz.utc)

            set_clause = ", ".join(
                f"{key} = ${i + 1}" for i, key in enumerate(update_data)
            )
            self._query_args = list(update_data.values())
            sql = f"UPDATE {self.table_name} SET {set_clause}"

            if where_lambda:
                where_clause_str = compile_expression(
                    where_lambda(Table()), self._query_args
                )
                sql += f" WHERE {where_clause_str}"
            elif self._where_clause:
                where_clause_str = compile_expression(
                    self._where_clause, self._query_args
                )
                sql += f" WHERE {where_clause_str}"
            else:
                raise ValueError(
                    "Update operation must include a WHERE clause to prevent full table update."
                )

            returning_fields = None
            if returning_fields_lambda:
                table = Table()
                returning_fields = returning_fields_lambda(table)

            if returning_fields:
                returning_clause = f" RETURNING {', '.join(compile_expression(field, []) for field in returning_fields)}"
                sql += returning_clause
                self.logger.info(
                    f"Executing UPDATE SQL with returning: {sql}, Args: {self._query_args}"
                )
                row = await self.db.fetchrow(sql, *self._query_args)
                return dict(row) if row else None
            else:
                sql += " RETURNING *"
                self.logger.info(
                    f"Executing UPDATE SQL with default returning: {sql}, Args: {self._query_args}"
                )
                row = await self.db.fetchrow(sql, *self._query_args)
                if row and self._can_return_model():
                    return self.model(**dict(row))
                elif row:
                    return dict(row)
                return None
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'update' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'update' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'update': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'update': {e}")
            raise
        finally:
            self.logger.debug("'update' method finished.")

    async def delete(
        self,
        where_lambda: Optional[Callable[[T], Expression]] = None,
    ) -> bool:
        """
        Asynchronously deletes records from the database based on a condition.

        This method takes an optional `where_lambda` to specify which records
        should be deleted. It is extremely important to provide a `where_lambda`
        to prevent accidental deletion of the entire table. The method returns
        `True` if the deletion was successful (no exceptions occurred), and
        `False` otherwise. Note that the return value does not indicate
        whether any rows were actually deleted, only the success of the
        database operation.

        Use Cases:
        1. Delete a user by their ID:
           ```python
           deleted = await query.where(lambda t: t.id == 123).delete()
           # Returns True if the delete operation was successful
           ```

        2. Delete all inactive users:
           ```python
           success = await query.where(lambda t: t.is_active == False).delete()
           # Returns True if the delete operation was successful
           ```

        3. Delete products with a price below a certain value:
           ```python
           deletion_successful = await query.where(lambda t: t.price < 50).delete()
           ```

        4. Delete records based on multiple conditions:
           ```python
           deleted_items = await query.where(lambda t: (t.category == 'old') & (t.removal_date < datetime.date(2025, 1, 1))).delete()
           ```

        5. Delete a single record based on a unique identifier (other than ID):
           ```python
           deleted_profile = await query.where(lambda t: t.username == "testuser").delete()
           ```

        6. Attempt to delete without a WHERE clause (raises ValueError):
           ```python
           try:
               await query.delete()
           except ValueError as e:
               print(f"Error: {e}")
           ```

        7. Delete records based on a date range:
           ```python
           deleted_logs = await query.where(lambda t: (t.log_date >= start_date) & (t.log_date <= end_date)).delete()
           ```

        8. Delete records where a certain field is NULL:
           ```python
           deleted_notes = await query.where(lambda t: t.comment == None).delete()
           ```

        9. Delete records based on a LIKE pattern:
           ```python
           deleted_temp_files = await query.where(lambda t: t.file_path.like('/tmp/%')).delete()
           ```

        10. Delete the most recent log entry (using ORDER BY and LIMIT 1):
            ```python
            # Note: This directly using delete might not be ideal with order/limit in all SQL dialects.
            # A safer approach might involve selecting the ID first and then deleting.
            # Example (conceptual):
            # latest_log = await query.order_by(lambda t: t.timestamp, order_type=OrderType.DESC).limit(1).get_one()
            # if latest_log:
            #     deleted = await query.where(lambda t: t.id == latest_log.id).delete()
            deleted = await query.where(lambda t: True).delete() # Placeholder
            ```

        11. Delete records based on a value in an array (if supported by the database):
            ```python
            # Example assuming array contains function
            # deleted_tagged = await query.where(lambda t: 'important'.in_(t.tags)).delete()
            deleted_tagged = await query.where(lambda t: True).delete() # Placeholder
            ```

        12. Delete records based on a condition involving a foreign key:
            ```python
            deleted_related = await query.where(lambda t: t.user_id == 5).delete()
            ```

        13. Delete records using a subquery in the WHERE clause (if supported by your ORM):
            ```python
            # Example of a conceptual subquery
            # deleted_old_orders = await query.where(lambda t: t.customer_id.in_(select(Customer.id).where(Customer.signup_date < ...))).delete()
            deleted_old_orders = await query.where(lambda t: True).delete() # Placeholder
            ```

        14. Delete all records in a table (only do this with extreme caution!):
            ```python
            # It's better to be explicit and potentially log this action heavily
            # deleted_all = await query.where(lambda t: True).delete()
            try:
                await query.delete() # This will raise a ValueError
            except ValueError as e:
                print(f"Error: {e}")
            ```

        15. Delete records and handle potential database errors:
            ```python
            try:
                deleted_unnecessary = await query.where(lambda t: t.status == 'temp').delete()
                if deleted_unnecessary:
                    print("Temporary records deleted.")
                else:
                    print("No temporary records found.")
            except PostgresError as e:
                print(f"Database error during deletion: {e}")
            ```

        16. Delete records based on a complex logical expression:
            ```python
            deleted_complex = await query.where(lambda t: (t.type == 'X') | ((t.type == 'Y') & (t.value < 100))).delete()
            ```

        17. Delete records and check the number of rows affected (this might require a different method depending on your database library):
            ```python
            # The current method returns a boolean, not the row count directly
            deleted = await query.where(lambda t: t.category == 'outdated').delete()
            # To get row count, you might need to execute a raw SQL query
            ```

        18. Delete records based on a case-insensitive comparison (if supported by the database):
            ```python
            # Example assuming a database function for case-insensitive comparison
            # deleted_case_insensitive = await query.where(lambda t: func.lower(t.name) == 'lowercase value').delete()
            deleted_case_insensitive = await query.where(lambda t: True).delete() # Placeholder
            ```

        19. Delete records where a field matches a list of values:
            ```python
            ids_to_delete = [1, 2, 3, 4, 5]
            deleted_multiple = await query.where(lambda t: t.id.in_(ids_to_delete)).delete()
            ```

        20. Delete records based on a condition involving a joined table (this would typically require a more complex query setup):
            ```python
            # Conceptual example requiring joins
            # await query.join(OtherTable, ...).where(...).delete()
            deleted_joined = await query.where(lambda t: True).delete() # Placeholder
            ```
        """
        self.logger.debug("Entering delete method.")
        try:
            if where_lambda is not None and not callable(where_lambda):
                raise TypeError("where_lambda must be a callable")

            sql = f"DELETE FROM {self.table_name}"
            self._query_args = []

            if where_lambda:
                where_clause_str = compile_expression(
                    where_lambda(Table()), self._query_args
                )
                sql += f" WHERE {where_clause_str}"
            elif self._where_clause:
                where_clause_str = compile_expression(
                    self._where_clause, self._query_args
                )
                sql += f" WHERE {where_clause_str}"
            else:
                raise ValueError(
                    "Delete operation must include a WHERE clause to prevent full table deletion."
                )

            self.logger.info(f"Executing DELETE SQL: {sql}, Args: {self._query_args}")
            try:
                await self.db.execute(sql, *self._query_args)
                return True
            except Exception as e:
                self.logger.error(f"Error executing DELETE SQL: {e}")
                return False
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'delete' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'delete' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'delete': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'delete': {e}")
            raise
        finally:
            self.logger.debug("'delete' method finished.")

    async def delete_by_id(self, id_val: Any, id_field: str = "id") -> bool:
        """
        Asynchronously deletes a single record by its unique identifier.

        This method provides a convenient way to delete a record based on its ID.
        It defaults to looking for a column named "id", but you can specify
        a different column name using the `id_field` parameter. It returns
        `True` if the deletion operation was successful, `False` otherwise.

        Use Cases:
        1. Delete a user by their ID (assuming the ID column is 'id'):
           ```python
           deleted = await query.delete_by_id(123)
           # Returns True if deletion was successful
           ```

        2. Delete a product by its product code:
           ```python
           deleted = await query.delete_by_id("ABC-456", id_field="product_code")
           # Returns True if deletion was successful
           ```

        3. Delete an order by its order number:
           ```python
           deleted = await query.delete_by_id(1001, id_field="order_number")
           # Returns True if deletion was successful
           ```

        4. Attempt to delete a non-existent user by ID:
           ```python
           deleted = await query.delete_by_id(9999)
           # Returns True even if no record was found to delete (operation successful)
           ```

        5. Delete a log entry by its unique log ID:
           ```python
           deleted = await query.delete_by_id(50, id_field="log_id")
           ```

        6. Delete a configuration setting by its key:
           ```python
           deleted = await query.delete_by_id("theme", id_field="key")
           ```

        7. Delete a record where the ID is not an integer:
           ```python
           deleted = await query.delete_by_id("unique-string", id_field="uuid")
           ```

        8. Handle cases where the specified ID field does not exist:
           ```python
           try:
               await query.delete_by_id(1, id_field="non_existent_field")
           except ValueError as e:
               print(f"Error: {e}")
           ```

        9. Delete a record based on a foreign key that acts as a unique identifier:
           ```python
           deleted_profile = await query.delete_by_id(789, id_field="profile_id")
           ```

        10. Delete a record using an indexed column as the identifier:
            ```python
            deleted_record = await query.delete_by_id("special-code", id_field="unique_code")
            ```

        11. Delete a record with an ID value of a different type (if compatible):
            ```python
            deleted_item = await query.delete_by_id("123", id_field="numeric_id")
            ```

        12. Attempt to delete a record with a null ID value (behavior depends on the database):
            ```python
            deleted_null = await query.delete_by_id(None)
            ```

        13. Delete a record using a case-sensitive ID (if the database is case-sensitive):
            ```python
            deleted_case_sensitive = await query.delete_by_id("CaseSensitive", id_field="case_sensitive_id")
            ```

        14. Delete a record where the ID is a date or timestamp:
            ```python
            import datetime
            deleted_event = await query.delete_by_id(datetime.date(2024, 1, 1), id_field="event_date")
            ```

        15. Delete a record using an ID that is part of a JSON structure (if supported):
            ```python
            # Requires querying within the JSON structure
            # Example (conceptual): await query.where(lambda t: t.json_data['id'] == 42).delete()
            deleted_json = await query.delete_by_id(42, id_field="json_data->>'id'") # Adjust syntax as needed
            ```

        16. Delete a record by an ID with leading/trailing whitespace:
            ```python
            deleted_spaced = await query.delete_by_id("  ID 2  ", id_field="spaced_id")
            ```

        17. Delete a record where the ID is a serialized value:
            ```python
            deleted_serialized = await query.delete_by_id("[4, 5]", id_field="serialized_id")
            ```

        18. Delete multiple records by different IDs using multiple calls:
            ```python
            await query.delete_by_id(201)
            await query.delete_by_id(202)
            # ...
            ```

        19. Delete a record based on a combined unique key (requires a different WHERE clause):
            ```python
            # Example: await query.where(lambda t: (t.user_id == 1) & (t.session_token == 'xyz')).delete()
            deleted_composite = await query.where(lambda t: True).delete() # Placeholder
            ```

        20. Delete a record and handle potential foreign key constraint errors:
            ```python
            try:
                deleted_parent = await query.delete_by_id(1)
            except PostgresError as e:
                print(f"Error deleting: {e}")
            ```
        """
        self.logger.debug("Entering delete_by_id method.")
        try:
            table = Table()
            if not hasattr(table, id_field):
                raise ValueError(
                    f"The object '{table.__class__.__name__}' does not have an attribute named '{id_field}'."
                )
            where_expression = getattr(table, id_field) == id_val
            return await self.delete(where_lambda=lambda t: where_expression)
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'delete_by_id' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'delete_by_id' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'delete_by_id': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'delete_by_id': {e}")
            raise
        finally:
            self.logger.debug("Finished 'delete_by_id' method.")

    async def exists(
        self,
        where_lambda: Optional[Callable[[T], Expression]] = None,
    ) -> bool:
        """
        Asynchronously checks if any records exist matching the given condition.

        This method executes a `SELECT EXISTS` query to efficiently determine
        if at least one record in the table satisfies the provided
        `where_lambda`. It returns `True` if such a record exists, and `False`
        otherwise. A `where_lambda` is strongly recommended for targeted checks.

        Use Cases:
        1. Check if a user with a specific ID exists:
           ```python
           user_exists = await query.exists(where_lambda=lambda t: t.id == 123)
           # Returns True if a user with ID 123 exists, False otherwise
           ```

        2. Check if any active users are present:
           ```python
           has_active_users = await query.exists(where_lambda=lambda t: t.is_active == True)
           ```

        3. Verify if a product with a given code exists:
           ```python
           product_available = await query.exists(where_lambda=lambda t: t.product_code == "XYZ-789")
           ```

        4. Check if any orders were placed today:
           ```python
           import datetime
           today = datetime.date.today()
           has_orders_today = await query.exists(where_lambda=lambda t: t.order_date == today)
           ```

        5. Verify if a record with multiple conditions exists:
           ```python
           item_found = await query.exists(where_lambda=lambda t: (t.category == 'A') & (t.status == 'pending'))
           ```

        6. Check if any records have a NULL value in a specific column:
           ```python
           has_null_notes = await query.exists(where_lambda=lambda t: t.notes == None)
           ```

        7. Check if any records match a LIKE pattern:
           ```python
           has_temp_files = await query.exists(where_lambda=lambda t: t.file_path.like('/tmp/%'))
           ```

        8. Verify if a user with a specific email address exists:
           ```python
           email_exists = await query.exists(where_lambda=lambda t: t.email == "test@example.com")
           ```

        9. Check if any records fall within a certain range:
           ```python
           value_in_range = await query.exists(where_lambda=lambda t: (t.value > 10) & (t.value < 20))
           ```

        10. Verify if any records have a boolean field set to True:
            ```python
            has_premium_users = await query.exists(where_lambda=lambda t: t.is_premium == True)
            ```

        11. Check if any records exist based on a value in an array (if supported):
            ```python
            # Example assuming array contains function
            # has_important_tag = await query.exists(where_lambda=lambda t: 'important'.in_(t.tags))
            has_important_tag = await query.exists(where_lambda=lambda t: True) # Placeholder
            ```

        12. Verify if any records are related to a specific foreign key:
            ```python
            has_comments_for_post = await query.exists(where_lambda=lambda t: t.post_id == 5)
            ```

        13. Check if any records exist based on a subquery (if supported):
            ```python
            # Conceptual example
            # has_old_customer_orders = await query.exists(where_lambda=lambda t: t.customer_id.in_(select(Customer.id).where(Customer.signup_date < ...)))
            has_old_customer_orders = await query.exists(where_lambda=lambda t: True) # Placeholder
            ```

        14. Attempt to use exists without a WHERE clause (raises ValueError):
            ```python
            try:
                await query.exists()
            except ValueError as e:
                print(f"Error: {e}")
            ```

        15. Check if any records have a specific JSON value (if supported):
            ```python
            # Example assuming JSON querying
            # has_dark_theme = await query.exists(where_lambda=lambda t: t.config['theme'] == 'dark')
            has_dark_theme = await query.exists(where_lambda=lambda t: True) # Placeholder
            ```

        16. Verify if any records have a length of a string field greater than a certain value:
            ```python
            has_long_descriptions = await query.exists(where_lambda=lambda t: func.length(t.description) > 200)
            ```

        17. Check if any records have a date in the future:
            ```python
            import datetime
            future_event_exists = await query.exists(where_lambda=lambda t: t.event_date > datetime.date.today())
            ```

        18. Verify if any records have a non-default value for a specific field:
            ```python
            has_custom_settings = await query.exists(where_lambda=lambda t: t.setting_value != 'default')
            ```

        19. Check if any records exist with a value in a specific set:
            ```python
            allowed_status = ['active', 'pending']
            has_allowed_status = await query.exists(where_lambda=lambda t: t.status.in_(allowed_status))
            ```

        20. Verify if any records exist based on a mathematical condition:
            ```python
            has_high_ratio = await query.exists(where_lambda=lambda t: (t.value1 / t.value2) > 2.0)
            ```
        """
        self.logger.debug("Entering exists method.")
        try:
            if where_lambda is not None and not callable(where_lambda):
                raise TypeError("where_lambda must be a callable")

            self._query_args = []
            if where_lambda:
                where_clause_str = compile_expression(
                    where_lambda(Table()), self._query_args
                )
            elif self._where_clause:
                where_clause_str = compile_expression(
                    self._where_clause, self._query_args
                )
            else:
                raise ValueError(
                    "Exists operation must include a WHERE clause to get correct response."
                )

            query = f"SELECT EXISTS (SELECT 1 FROM {self.table_name} WHERE {where_clause_str})"
            self.logger.info(f"Executing EXISTS SQL: {query}, Args: {self._query_args}")
            result = await self.db.fetchrow(query, *self._query_args)
            return result[0] if result else False
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'exists' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'exists' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'exists': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'exists': {e}")
            raise
        finally:
            self.logger.debug("'exists' method finished.")

    async def values(
        self,
        columns_lambda: Callable[[T], List[Union[TableField, str]]],
        where_lambda: Optional[Callable[[T], Expression]] = None,
    ) -> List[dict]:
        """
        Asynchronously retrieves specific columns from the database as a list of dictionaries.

        This method allows you to select a subset of columns from the table
        and returns the results as a list where each element is a dictionary
        mapping the column name to its value. You can also apply an optional
        `where_lambda` to filter the rows. This is useful when you only need
        certain data fields and want a lightweight result set.

        Use Cases:
        1. Get a list of usernames and emails for all users:
           ```python
           user_details = await query.values(columns_lambda=lambda t: [t.username, t.email])
           # Returns a list of dictionaries like [{'username': '...', 'email': '...'}, ...]
           ```

        2. Get a list of product names and prices for active products:
           ```python
           active_product_info = await query.values(columns_lambda=lambda t: [t.name, t.price], where_lambda=lambda t: t.is_active == True)
           ```

        3. Retrieve only the email addresses of all users:
           ```python
           user_emails = await query.values(columns_lambda=lambda t: [t.email])
           # Returns a list of dictionaries like [{'email': '...'}, ...]
           ```

        4. Get the IDs and order dates for orders placed in a specific month:
           ```python
           import datetime
           start_date = datetime.date(2025, 5, 1)
           end_date = datetime.date(2025, 5, 31)
           may_order_info = await query.values(columns_lambda=lambda t: [t.id, t.order_date], where_lambda=lambda t: (t.order_date >= start_date) & (t.order_date <= end_date))
           ```

        5. Retrieve the names of all categories:
           ```python
           category_names = await query.values(columns_lambda=lambda t: [t.name])
           ```

        6. Get the titles and creation dates of the latest 10 blog posts:
           ```python
           latest_post_info = await query.order_by(lambda t: t.created_at, order_type=OrderType.DESC).limit(10).values(columns_lambda=lambda t: [t.title, t.created_at])
           ```

        7. Retrieve distinct product categories:
           ```python
           distinct_categories = await query.distinct().values(columns_lambda=lambda t: [t.category])
           ```

        8. Get the user IDs and the count of their posts (requires GROUP BY and aggregation):
           ```python
           # Note: This might require a more complex query using .select() with func.count()
           # Example (conceptual): await query.group_by(lambda t: [t.user_id]).select(lambda t: [t.user_id, func.count(t.post_id)]).get_all()
           user_post_counts = await query.values(columns_lambda=lambda t: [t.user_id]) # Placeholder for a more complex query
           ```

        9. Retrieve specific fields for records matching a LIKE condition:
           ```python
           partial_logs = await query.values(columns_lambda=lambda t: [t.timestamp, t.message], where_lambda=lambda t: t.message.like('%error%'))
           ```

        10. Get a list of only the primary keys of all records:
            ```python
            all_ids = await query.values(columns_lambda=lambda t: [t.id])
            ```

        11. Retrieve two related foreign key IDs:
            ```python
            link_info = await query.values(columns_lambda=lambda t: [t.user_id, t.role_id], where_lambda=lambda t: t.is_active == True)
            ```

        12. Get a specific column for records within a certain ID range:
            ```python
            names_in_range = await query.values(columns_lambda=lambda t: [t.name], where_lambda=lambda t: (t.id >= 50) & (t.id <= 100))
            ```

        13. Retrieve data for a specific set of IDs:
            ```python
            target_ids = [10, 20, 30]
            selected_data = await query.values(columns_lambda=lambda t: [t.data_field], where_lambda=lambda t: t.id.in_(target_ids))
            ```

        14. Get a single column's values where another column meets a condition:
            ```python
            emails_for_premium = await query.values(columns_lambda=lambda t: [t.email], where_lambda=lambda t: t.is_premium == True)
            ```

        15. Retrieve aliased column names:
            ```python
            aliased_data = await query.select(lambda t: [t.old_name.label("new_name")]).values(columns_lambda=lambda t: ["new_name"])
            ```

        16. Get values from records ordered by a specific column:
            ```python
            ordered_prices = await query.order_by(lambda t: t.price).values(columns_lambda=lambda t: [t.price])
            ```

        17. Retrieve data with a secondary sort order:
            ```python
            sorted_data = await query.order_by(lambda t: t.group).then_by(lambda t: t.sort_order).values(columns_lambda=lambda t: [t.group, t.sort_order])
            ```

        18. Get values based on a condition involving a function:
            ```python
            # Example assuming a database function
            # lowercase_names = await query.values(columns_lambda=lambda t: [func.lower(t.name)], where_lambda=lambda t: t.is_active == True)
            lowercase_names = await query.values(columns_lambda=lambda t: [t.name], where_lambda=lambda t: t.is_active == True) # Placeholder
            ```

        19. Retrieve values after applying a limit:
            ```python
            limited_results = await query.limit(5).values(columns_lambda=lambda t: [t.id, t.status])
            ```

        20. Get values with a combination of filtering and ordering:
            ```python
            filtered_ordered_data = await query.where(lambda t: t.category == 'B').order_by(lambda t: t.value, order_type=OrderType.DESC).values(columns_lambda=lambda t: [t.item_id, t.value])
            ```
        """
        self.logger.debug("Entering values method.")
        try:
            if not callable(columns_lambda):
                raise TypeError("columns_lambda must be a callable")

            if where_lambda is not None and not callable(where_lambda):
                raise TypeError("where_lambda must be a callable")

            self.select(columns_lambda)
            if where_lambda:
                self.where(where_lambda)
            return await self.get_all()
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'values' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'values' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'values': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'values': {e}")
            raise
        finally:
            self.logger.debug("'values' method finished.")

    async def first_or_none(
        self, where_lambda: Optional[Callable[[T], Expression]] = None
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Asynchronously retrieves the first record matching the condition, or None if no match is found.

        This method is useful for fetching a single record when you expect at most one result.
        It applies an optional `where_lambda` to filter the records and then returns the first one.
        If no records match the criteria, it returns `None`.

        Use Cases:
        1. Get the user with a specific ID, or None if not found:
           ```python
           user = await query.first_or_none(where_lambda=lambda t: t.id == 123)
           # Returns a User object or None
           ```

        2. Get the first active user, or None if no active users exist:
           ```python
           first_active_user = await query.first_or_none(where_lambda=lambda t: t.is_active == True)
           ```

        3. Retrieve a product by its unique code, or None if the code is invalid:
           ```python
           product = await query.first_or_none(where_lambda=lambda t: t.product_code == "ABC-789")
           ```

        4. Get the most recently created record (requires ordering):
           ```python
           latest_record = await query.order_by(lambda t: t.created_at, order_type=OrderType.DESC).first_or_none()
           ```

        5. Find the first record matching multiple criteria:
           ```python
           item = await query.first_or_none(where_lambda=lambda t: (t.category == 'A') & (t.status == 'pending'))
           ```

        6. Retrieve the first record where a specific field is NULL:
           ```python
           first_null_note = await query.first_or_none(where_lambda=lambda t: t.notes == None)
           ```

        7. Get the first record matching a LIKE pattern:
           ```python
           first_temp_file = await query.first_or_none(where_lambda=lambda t: t.file_path.like('/tmp/%'))
           ```

        8. Find a user by their email address:
           ```python
           user_by_email = await query.first_or_none(where_lambda=lambda t: t.email == "test@example.com")
           ```

        9. Retrieve the first record within a certain range:
           ```python
           first_in_range = await query.first_or_none(where_lambda=lambda t: (t.value > 10) & (t.value < 20))
           ```

        10. Get the first premium user:
            ```python
            first_premium = await query.first_or_none(where_lambda=lambda t: t.is_premium == True)
            ```

        11. Retrieve the first record with a specific value in an array (if supported):
            ```python
            # Example assuming array contains function
            # first_important_tag = await query.first_or_none(where_lambda=lambda t: 'important'.in_(t.tags))
            first_important_tag = await query.first_or_none(where_lambda=lambda t: True) # Placeholder
            ```

        12. Find the first comment for a specific post:
            ```python
            first_comment = await query.first_or_none(where_lambda=lambda t: t.post_id == 5)
            ```

        13. Retrieve the first record based on a subquery (if supported):
            ```python
            # Conceptual example
            # first_old_customer_order = await query.first_or_none(where_lambda=lambda t: t.customer_id.in_(select(Customer.id).where(Customer.signup_date < ...)))
            first_old_customer_order = await query.first_or_none(where_lambda=lambda t: True) # Placeholder
            ```

        14. Attempt to get the first record without any WHERE clause (returns the very first record in the table or None if empty):
            ```python
            first_record = await query.first_or_none()
            ```

        15. Retrieve the first record with a specific JSON value (if supported):
            ```python
            # Example assuming JSON querying
            # first_dark_theme = await query.first_or_none(where_lambda=lambda t: t.config['theme'] == 'dark')
            first_dark_theme = await query.first_or_none(where_lambda=lambda t: True) # Placeholder
            ```

        16. Get the first record where the length of a string field exceeds a value:
            ```python
            first_long_description = await query.first_or_none(where_lambda=lambda t: func.length(t.description) > 200)
            ```

        17. Retrieve the first event on or after a specific date:
            ```python
            import datetime
            start_of_year = datetime.date(2025, 1, 1)
            first_event_this_year = await query.first_or_none(where_lambda=lambda t: t.event_date >= start_of_year)
            ```

        18. Find the first record with a non-default setting:
            ```python
            first_custom_setting = await query.first_or_none(where_lambda=lambda t: t.setting_value != 'default')
            ```

        19. Get the first record with a status in a specific list:
            ```python
            valid_statuses = ['active', 'pending']
            first_valid_status = await query.first_or_none(where_lambda=lambda t: t.status.in_(valid_statuses))
            ```

        20. Retrieve the first record based on a mathematical condition:
            ```python
            first_high_ratio = await query.first_or_none(where_lambda=lambda t: (t.value1 / t.value2) > 2.0)
            ```
        """
        self.logger.debug("Entering first_or_none method.")
        try:
            if where_lambda is not None and not callable(where_lambda):
                raise TypeError("where_lambda must be a callable")

            query = self
            if where_lambda:
                query = query.where(where_lambda)
            query._limit_clause = 1
            sql, args = query.compile()
            self.logger.info(f"Executing SQL for first_or_none(): {sql}, Args: {args}")
            result = await self.db.fetchrow(sql, *args)
            if result:
                return (
                    self.model(**dict(result))
                    if self._can_return_model()
                    else dict(result)
                )
            return None
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'first_or_none' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'first_or_none' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'first_or_none': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'first_or_none': {e}")
            raise
        finally:
            self.logger.debug("'first_or_none' method finished.")

    async def last_or_none(
        self, where_lambda: Optional[Callable[[T], Expression]] = None
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Asynchronously retrieves the last record matching the condition, or None if no match is found.

        This method is useful for fetching a single record when you need the last one based on a specific order.
        It requires an `ORDER BY` clause to be set on the query. It applies an optional `where_lambda`
        to filter the records, reverses the order, limits the result to one, and then returns that record.
        If no records match the criteria, it returns `None`. The original order is restored after the operation.

        Use Cases:
        1. Get the most recently modified user:
           ```python
           last_modified_user = await query.order_by(lambda t: t.updated_at, order_type=OrderType.DESC).last_or_none()
           # Returns the User object with the latest updated_at or None
           ```

        2. Get the last logged-in user:
           ```python
           last_login = await query.order_by(lambda t: t.last_login_time, order_type=OrderType.DESC).last_or_none(where_lambda=lambda t: t.is_online == True)
           ```

        3. Retrieve the product with the highest price:
           ```python
           most_expensive_product = await query.order_by(lambda t: t.price, order_type=OrderType.DESC).last_or_none()
           ```

        4. Get the last record created within a specific date range:
           ```python
           import datetime
           start = datetime.date(2025, 1, 1)
           end = datetime.date(2025, 1, 31)
           last_january_record = await query.where(lambda t: (t.created_at >= start) & (t.created_at <= end)).order_by(lambda t: t.created_at, order_type=OrderType.DESC).last_or_none()
           ```

        5. Find the last record matching multiple criteria, ordered by a specific field:
           ```python
           last_pending_item = await query.where(lambda t: (t.category == 'B') & (t.status == 'pending')).order_by(lambda t: t.priority, order_type=OrderType.DESC).last_or_none()
           ```

        6. Retrieve the last record where a specific field is not NULL, ordered by creation time:
           ```python
           last_non_null_note = await query.where(lambda t: t.notes != None).order_by(lambda t: t.created_at, order_type=OrderType.DESC).last_or_none()
           ```

        7. Get the last log entry matching a LIKE pattern, ordered by timestamp:
           ```python
           last_error_log = await query.where(lambda t: t.message.like('%error%')).order_by(lambda t: t.timestamp, order_type=OrderType.DESC).last_or_none()
           ```

        8. Find the user with the alphabetically last username:
           ```python
           last_user_alpha = await query.order_by(lambda t: t.username, order_type=OrderType.DESC).last_or_none()
           ```

        9. Retrieve the record with the smallest value (using DESC order and then getting the last):
           ```python
           smallest_value_record = await query.order_by(lambda t: t.value).last_or_none()
           ```

        10. Get the last premium user who signed up:
            ```python
            last_premium_signup = await query.where(lambda t: t.is_premium == True).order_by(lambda t: t.signup_date, order_type=OrderType.DESC).last_or_none()
            ```

        11. Retrieve the last record with a specific tag, ordered by relevance:
            ```python
            # Assuming a 'relevance' field
            last_relevant_tag = await query.where(lambda t: 'important'.in_(t.tags)).order_by(lambda t: t.relevance, order_type=OrderType.DESC).last_or_none()
            ```

        12. Find the last comment for a specific post, ordered by creation time:
            ```python
            last_comment = await query.where(lambda t: t.post_id == 5).order_by(lambda t: t.created_at, order_type=OrderType.DESC).last_or_none()
            ```

        13. Retrieve the last record based on a subquery result (requires careful ordering):
            ```python
            # Conceptual example: last order by a specific group of customers
            # last_group_order = await query.where(lambda t: t.customer_id.in_(select(...))).order_by(t.order_date.desc()).last_or_none()
            last_group_order = await query.order_by(lambda t: t.id).last_or_none(where_lambda=lambda t: True) # Placeholder
            ```

        14. Attempt to use last_or_none without setting an ORDER BY clause (raises ValueError):
            ```python
            try:
                await query.last_or_none()
            except ValueError as e:
                print(f"Error: {e}")
            ```

        15. Retrieve the last record with a specific JSON setting, ordered by ID:
            ```python
            # Example assuming JSON querying
            # last_dark_theme_config = await query.where(lambda t: t.config['theme'] == 'dark').order_by(t.id.desc()).last_or_none()
            last_dark_theme_config = await query.order_by(lambda t: t.id, order_type=OrderType.DESC).last_or_none(where_lambda=lambda t: True) # Placeholder
            ```

        16. Get the last record with a long description, ordered alphabetically by title:
            ```python
            last_long_desc_alpha = await query.where(lambda t: func.length(t.description) > 200).order_by(lambda t: t.title, order_type=OrderType.DESC).last_or_none()
            ```

        17. Retrieve the last event before a specific date, ordered by event time:
            ```python
            import datetime
            cutoff_date = datetime.date(2025, 6, 1)
            last_event_before_june = await query.where(lambda t: t.event_date < cutoff_date).order_by(lambda t: t.event_date, order_type=OrderType.DESC).last_or_none()
            ```

        18. Find the last record with a non-default value for a setting, ordered by key:
            ```python
            last_custom_setting_alpha = await query.where(lambda t: t.setting_value != 'default').order_by(lambda t: t.key, order_type=OrderType.DESC).last_or_none()
            ```

        19. Get the last record with a status in a specific list, ordered by update time:
            ```python
            valid_statuses = ['active', 'pending']
            last_valid_status_update = await query.where(lambda t: t.status.in_(valid_statuses)).order_by(lambda t: t.updated_at, order_type=OrderType.DESC).last_or_none()
            ```

        20. Retrieve the last record based on a mathematical condition, ordered by ID:
            ```python
            last_high_ratio_record = await query.where(lambda t: (t.value1 / t.value2) > 2.0).order_by(lambda t: t.id, order_type=OrderType.DESC).last_or_none()
            ```
        """
        self.logger.debug("Entering last_or_none method.")
        try:
            if where_lambda is not None and not callable(where_lambda):
                raise TypeError("where_lambda must be a callable")

            if self._order_by_clause is None:
                raise ValueError("Cannot use `last_or_none` without an ORDER BY clause")
            original_order_by = self._order_by_clause
            self._order_by_clause = self._reverse_order_clause(self._order_by_clause)
            query = self
            if where_lambda:
                query = query.where(where_lambda)
            query._limit_clause = 1
            sql, args = query.compile()
            self.logger.info(f"Executing SQL for last_or_none(): {sql}, Args: {args}")
            result = await self.db.fetchrow(sql, *args)
            self._order_by_clause = original_order_by
            if result:
                return (
                    self.model(**dict(result))
                    if self._can_return_model()
                    else dict(result)
                )
            return None
        except ValueError as e:
            self.logger.exception(f"Invalid argument in 'last_or_none' method: {e}")
            raise
        except TypeError as e:
            self.logger.exception(f"Invalid type in 'last_or_none' method: {e}")
            raise
        except PostgresError as e:
            self.logger.exception(f"Database error during 'last_or_none': {e}")
            raise
        except Exception as e:
            self.logger.exception(f"Unexpected error in 'last_or_none': {e}")
            raise
        finally:
            self.logger.debug("'last_or_none' method finished.")

    def _reverse_order_clause(self, order_by_clause: str) -> str:
        """Reverses the direction of ordering in the given ORDER BY clause.

        For each field in the clause, if the direction is ASC, it's changed to
        DESC, and vice versa. If no direction is specified, it defaults to
        ASC and is then reversed to DESC.

        Args:
            order_by_clause (str): The original ORDER BY clause string.

        Returns:
            str: The ORDER BY clause with reversed ordering directions.
        """
        parts = [part.strip() for part in order_by_clause.split(",")]
        reversed_parts = []
        for part in parts:
            sub_parts = part.split()
            field = sub_parts[0]
            direction = sub_parts[1].upper() if len(sub_parts) > 1 else "ASC"
            reversed_direction = "DESC" if direction == "ASC" else "ASC"
            reversed_parts.append(f"{field} {reversed_direction}")
        return ", ".join(reversed_parts)

    def _can_return_model(self) -> bool:
        """
        Checks if the current query allows returning a model instance.

        Returns True if a model can be returned, False otherwise. This depends
        on whether there are GROUP BY clauses, if specific fields (and all
        required fields, if defined in the model) are selected, and if
        aggregate functions are used in the selection.
        """
        if self._group_by_fields:
            return False
        if not self._select_fields:
            return True
        if any(isinstance(field, Function) for field in self._select_fields):
            return False
        if hasattr(self.model, "__required_fields__"):
            required_fields = getattr(self.model, "__required_fields__", [])
            selected_field_names = {
                field.name if isinstance(field, TableField) else field.alias
                for field in self._select_fields
            }
            return all(rf in selected_field_names for rf in required_fields)
        else:
            return bool(self._select_fields)


class PagedResults(Generic[T]):
    def __init__(
        self, items: List[T], total_count: int, page_number: int, page_size: int
    ):
        self.items = items
        self.total_count = total_count
        self.page_number = page_number
        self.page_size = page_size
        self.total_pages = math.ceil(total_count / page_size) if page_size > 0 else 0
        self.has_previous_page = page_number > 1
        self.has_next_page = page_number < self.total_pages
        self.is_first_page = page_number == 1
        self.is_last_page = (
            page_number == self.total_pages if self.total_pages > 0 else True
        )
        self.first_item_on_page = (
            (page_number - 1) * page_size + 1 if total_count > 0 else 0
        )
        self.last_item_on_page = (
            min(page_number * page_size, total_count) if total_count > 0 else 0
        )

    def __repr__(self):
        return (
            f"<PagedResults(page={self.page_number}, size={self.page_size}, "
            f"total={self.total_count}, items_count={len(self.items)})>"
        )
