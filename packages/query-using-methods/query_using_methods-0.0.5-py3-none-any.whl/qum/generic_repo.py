from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Generic,
    List,
    Optional,
    Callable,
    Union,
)
from loguru import logger

from qum.expressions import Expression, Table, TableField
from qum.query import PagedResults, Query
from qum.database import Database
from qum.enums import OrderType

T = TypeVar("T")


class GenericRepository(Generic[T]):
    """
    Generic repository class for interacting with a database table.  Provides
    CRUD operations and other common data access patterns.
    """

    def __init__(
        self, db: Database, table_name: str, model: Type[T], primary_key: str = "id"
    ):
        """
        Initializes the repository.

        Args:
            db: The database connection.
            table_name: The name of the database table.
            model: The SQLAlchemy model class associated with the table.
            primary_key: The name of the primary key column.
        """
        if not isinstance(db, Database):
            raise TypeError("db must be an instance of Database")
        if not isinstance(table_name, str) or not table_name.strip():
            raise ValueError("table_name must be a non-empty string")
        if not isinstance(model, type):
            raise TypeError("model must be a class")
        if not isinstance(primary_key, str):
            raise TypeError("primary_key must be a string")

        self.db = db
        self.table_name = table_name
        self.model = model
        self.primary_key = primary_key
        self.logger = logger  # Using the imported logger

    def _get_query(self) -> Query[T]:
        """
        Returns a new Query object for the current table and model.
        """
        return Query[T](self.table_name, self.model, self.db, self.logger)

    async def get(
        self,
        where_lambda: Optional[Callable[[T], Expression]] = None,
        order_by_lambda: Optional[Callable[[T], TableField]] = None,
        order_type: OrderType = None,
        then_by_lambda: Optional[Callable[[T], TableField]] = None,
        then_type: OrderType = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        distinct: bool = False,
        columns_lambda: Optional[Callable[[T], List[Union[TableField, str]]]] = None,
    ) -> Union[List[T], List[Dict[str, Any]]]:
        """
        Retrieves records from the database based on specified criteria.

        Args:
            where_lambda:  A lambda function to define the WHERE clause.
            order_by_lambda: A lambda function to define the ORDER BY clause.
            order_type: The order type (ASC or DESC).
            then_by_lambda: A lambda for secondary ordering.
            then_type: The order type for the secondary ordering.
            limit: The maximum number of records to retrieve.
            offset: The starting position of the records to retrieve.
            distinct: Whether to retrieve distinct records.
            columns_lambda: A lambda to select specific columns.

        Returns:
            A list of model instances or dictionaries.
        """
        query = self._get_query()
        return await query.get(
            where_lambda,
            order_by_lambda,
            order_type,
            then_by_lambda,
            then_type,
            limit,
            offset,
            distinct,
            columns_lambda,
        )

    async def get_one(
        self, where_lambda: Optional[Callable[[T], Expression]] = None
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Retrieves a single record from the database.

        Args:
            where_lambda: A lambda function to define the WHERE clause.

        Returns:
            A single model instance or dictionary, or None if no record is found.
        """
        query = self._get_query()
        if where_lambda:
            query = query.where(where_lambda)
        return await query.get_one()

    async def get_by_id(self, id: Any) -> Optional[T]:
        """
        Retrieves a record by its primary key.

        Args:
            id: The value of the primary key.

        Returns:
            The model instance if found, otherwise None.
        """
        query = self._get_query()
        return await query.get_by_id(id_val=id, id_field=self.primary_key)

    async def get_all(self) -> List[Union[T, Dict[str, Any]]]:
        """
        Retrieves all records from the database table.

        Returns:
            A list of model instances or dictionaries.
        """
        query = self._get_query()
        return await query.get_all()

    async def get_pages(
        self,
        where_lambda: Optional[Callable[[T], Expression]] = None,
        order_by_lambda: Optional[Callable[[T], TableField]] = None,
        order_type: OrderType = None,
        then_by_lambda: Optional[Callable[[T], TableField]] = None,
        then_type: OrderType = None,
        page: int = 1,
        page_size: int = 10,
        distinct: bool = False,
        columns_lambda: Optional[Callable[[T], List[Union[TableField, str]]]] = None,
    ) -> PagedResults[T]:
        """
        Retrieves records from the database in a paginated fashion.

        Args:
            where_lambda: A lambda function to define the WHERE clause.
            order_by_lambda:  A lambda function to define the ORDER BY clause.
            order_type: The order type (ASC or DESC).
            then_by_lambda: A lambda for secondary ordering.
            then_type: The order type for the secondary ordering.
            page: The page number.
            page_size: The number of records per page.
            distinct: Whether to retrieve distinct records.
            columns_lambda: A lambda to select specific columns.

        Returns:
            A PagedResults object containing the items, total count, and pagination information.
        """
        query = self._get_query()
        return await query.get_pages(
            where_lambda,
            order_by_lambda,
            order_type,
            then_by_lambda,
            then_type,
            page,
            page_size,
            distinct,
            columns_lambda,
        )

    async def create(
        self,
        data: T,
        returning_fields_lambda: Optional[
            Callable[[T], List[Union[TableField, str]]]
        ] = None,
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Creates a new record in the database.

        Args:
            data: The data for the new record (model instance).
            returning_fields_lambda: A lambda to specify which fields to return.

        Returns:
            The created record (model instance or dictionary), or None on failure.
        """
        query = self._get_query()
        return await query.create(data, returning_fields_lambda)

    async def bulk_create(self, data_list: List[T]) -> int:
        """
        Inserts multiple records into the database efficiently.

        Args:
            data_list: A list of model instances to insert.

        Returns:
            The number of rows successfully inserted.
        """
        query = self._get_query()
        return await query.bulk_create(data_list)

    async def update_fields(
        self,
        data: Dict[str, Any],
        where_lambda: Optional[Callable[[T], Expression]] = None,
        returning_fields_lambda: Optional[
            Callable[[T], List[Union[TableField, str]]]
        ] = None,
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Updates records in the database based on a WHERE clause.  Use this
        for partial updates.

        Args:
            data: A dictionary containing the fields and values to update.
            where_lambda: A lambda function to define the WHERE clause.
            returning_fields_lambda: A lambda to specify which fields to return
        Returns:
            The updated record (model instance or dictionary), or None on failure.
        """
        query = self._get_query()
        return await query.update(data, where_lambda, returning_fields_lambda)

    async def update(self, entity: T) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Updates an existing record in the database using the provided entity.
        This method assumes the entity has the primary key value set.

        Args:
            entity: The updated entity (model instance).

        Returns:
            The updated record (model instance or dictionary), or None on failure.
        Raises:
            ValueError: If the entity does not have the primary key set.
        """
        entity_dict = (
            entity.__dict__.copy()
        )  # Create a copy to avoid modifying the original object
        pk = entity_dict.get(self.primary_key)
        if pk is None:
            raise ValueError(
                f"Entity must have the primary key '{self.primary_key}' set for update"
            )
        del entity_dict[self.primary_key]  # Remove primary key from the update data
        query = self._get_query()
        return await query.update(
            entity_dict, lambda t: getattr(t, self.primary_key) == pk
        )

    async def delete(
        self, where_lambda: Optional[Callable[[T], Expression]] = None
    ) -> bool:
        """
        Deletes records from the database based on a WHERE clause.

        Args:
            where_lambda: A lambda function to define the WHERE clause.

        Returns:
            True if the deletion was successful, False otherwise.
        """
        query = self._get_query()
        return await query.delete(where_lambda)

    async def delete_by_id(self, id: Any) -> bool:
        """
        Deletes a record by its primary key.

        Args:
            id: The value of the primary key.

        Returns:
            True if the deletion was successful, False otherwise.
        """
        query = self._get_query()
        return await query.delete_by_id(id_val=id, id_field=self.primary_key)

    async def exists(
        self, where_lambda: Optional[Callable[[T], Expression]] = None
    ) -> bool:
        """
        Checks if any records exist matching the given WHERE clause.

        Args:
            where_lambda: A lambda function to define the WHERE clause.

        Returns:
            True if any matching records exist, False otherwise.
        """
        query = self._get_query()
        return await query.exists(where_lambda)

    async def exists_by_id(self, id: Any) -> bool:
        """
        Checks if a record with the given primary key exists.

        Args:
            id: The value of the primary key.

        Returns:
            True if a matching record exists, False otherwise.
        """
        return await self.exists(lambda t: getattr(t, self.primary_key) == id)

    async def values(
        self,
        columns_lambda: Callable[[T], List[Union[TableField, str]]],
        where_lambda: Optional[Callable[[T], Expression]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves data from the table as a list of dictionaries, with optional
        filtering.

        Args:
            columns_lambda: A lambda function to select the columns.
            where_lambda: An optional lambda function to filter the results.

        Returns:
            A list of dictionaries, where each dictionary represents a row.
        """
        query = self._get_query()
        return await query.values(columns_lambda, where_lambda)

    async def first_or_none(
        self, where_lambda: Optional[Callable[[T], Expression]] = None
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Retrieves the first record that matches the given criteria, or None if no
        records match.

        Args:
            where_lambda: A lambda function to define the WHERE clause.

        Returns:
            The first matching record (model instance or dictionary), or None.
        """
        query = self._get_query()
        return await query.first_or_none(where_lambda)

    async def last_or_none(
        self,
        where_lambda: Optional[Callable[[T], Expression]] = None,
        order_by_lambda: Optional[Callable[[T], TableField]] = None,
        order_type: OrderType = OrderType.ASC,
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Retrieves the last record that matches the given criteria, or None if no
        records match.  Requires an ORDER BY clause.

        Args:
            where_lambda: A lambda function to define the WHERE clause.
            order_by_lambda: A lambda function to define the ORDER BY clause.
            order_type: The order type (ASC or DESC).

        Returns:
            The last matching record (model instance or dictionary), or None.
        Raises:
            ValueError: If order_by_lambda is not provided.
        """
        if not order_by_lambda:
            raise ValueError("last_or_none requires an order_by_lambda")
        query = self._get_query()
        query = query.order_by(order_by_lambda, order_type)  # Set the order
        return await query.last_or_none(where_lambda)

    # Aggregate function methods
    async def count(
        self,
        field: str = "*",
        alias: str = "count",
        where_lambda: Optional[Callable[[T], Expression]] = None,
    ) -> Optional[int]:
        """
        Counts the number of records, optionally filtered by a WHERE clause.

        Args:
            field: The field to count (default: "*").
            alias: The alias for the count (default: "count").
            where_lambda: An optional lambda function to filter the results.

        Returns:
            The count.
        """
        query = self._get_query()
        table = Table()
        query.select(lambda t: [table.count(field=getattr(table, field), alias=alias)])

        if where_lambda:
            query.where(where_lambda)
        count_dict = await query.get_one()
        return count_dict.get(alias)

    async def sum(
        self,
        field: str,
        alias: str = "sum",
        where_lambda: Optional[Callable[[T], Expression]] = None,
    ) -> Optional[float]:
        """
        Calculates the sum of a numeric field.

        Args:
            field: The name of the numeric field.
            alias: The alias for the sum (default: "sum").
             where_lambda: An optional lambda function to filter the results.

        Returns:
            The sum, or None if there are no matching records.
        """

        query = self._get_query()
        table = Table()
        query.select(lambda t: [table.sum(field=getattr(table, field), alias=alias)])

        if where_lambda:
            query.where(where_lambda)
        count_dict = await query.get_one()
        return count_dict.get(alias)

    async def avg(
        self,
        field: str,
        alias: str = "avg",
        where_lambda: Optional[Callable[[T], Expression]] = None,
    ) -> Optional[float]:
        """
        Calculates the average of a numeric field.

        Args:
            field: The name of the numeric field.
            alias: The alias for the average (default: "avg").
            where_lambda: An optional lambda function to filter the results.

        Returns:
            The average, or None if there are no matching records.
        """

        query = self._get_query()
        table = Table()
        query.select(lambda t: [table.avg(field=getattr(table, field), alias=alias)])

        if where_lambda:
            query.where(where_lambda)
        count_dict = await query.get_one()
        return count_dict.get(alias)

    async def min(
        self,
        field: str,
        alias: str = "min",
        where_lambda: Optional[Callable[[T], Expression]] = None,
    ) -> Optional[Any]:
        """
        Finds the minimum value of a field.

        Args:
            field: The name of the field.
            alias: The alias for the minimum (default: "min").
            where_lambda: An optional lambda function to filter the results.

        Returns:
            The minimum value, or None if there are no matching records.
        """
        query = self._get_query()
        table = Table()
        query.select(lambda t: [table.min(field=getattr(table, field), alias=alias)])

        if where_lambda:
            query.where(where_lambda)
        count_dict = await query.get_one()
        return count_dict.get(alias)

    async def max(
        self,
        field: str,
        alias: str = "max",
        where_lambda: Optional[Callable[[T], Expression]] = None,
    ) -> Optional[Any]:
        """
        Finds the maximum value of a field.

        Args:
            field: The name of the field.
            alias: The alias for the maximum (default: "max").
            where_lambda: An optional lambda function to filter the results.

        Returns:
            The maximum value, or None if there are no matching records.
        """
        query = self._get_query()
        table = Table()
        query.select(lambda t: [table.max(field=getattr(table, field), alias=alias)])

        if where_lambda:
            query.where(where_lambda)
        count_dict = await query.get_one()
        return count_dict.get(alias)
