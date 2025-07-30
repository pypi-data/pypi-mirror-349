from typing import List, Optional
import asyncpg
from loguru import logger


class Database:
    """
    A class for managing asynchronous connections to a PostgreSQL database.
    It handles connection pooling, executing queries, and fetching results.
    """

    def __init__(
        self,
        host: str,
        port: int,
        name: str,
        user: str,
        password: str,
        min_size: int,
        max_size: int,
        command_timeout: int,
    ):
        """
        Initializes the Database instance with connection pool parameters.
        """
        self.pool: Optional[asyncpg.Pool] = None

        self.host = host
        self.port = port
        self.database = name
        self.user = user
        self.password = password or None
        self.min_size = min_size
        self.max_size = max_size
        self.command_timeout = command_timeout

    async def connect(self, create_tables_list_if_needed: List[str] = []):
        """
        Establishes a connection pool to the PostgreSQL database using the
        configuration settings from the `config` module. It also calls the
        internal method to create the necessary tables if they don't exist.

        Raises:
            Exception: If there is an error during the connection attempt.
        """
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                min_size=self.min_size,
                max_size=self.max_size,
                command_timeout=self.command_timeout,
                statement_cache_size=0,  # Can improve performance in some scenarios
            )
            logger.info("Successfully connected to PostgreSQL!")
            await self._create_tables(create_tables_list_if_needed)
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL: {e}", exc_info=True)
            raise

    async def _create_tables(self, create_tables_list_if_needed: List[str]):
        """
        Internal method to check for the existence of the 'users' and 'chats'
        tables and create them if they are not present. It uses the SQL schema
        definitions from the `database.create_tables` module.
        """
        logger.debug("Checking for and creating necessary tables...")
        for table in create_tables_list_if_needed:
            await self._execute(table)
        logger.debug("Table creation check completed.")

    async def disconnect(self):
        """
        Closes the PostgreSQL connection pool if it is currently active.
        """
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL connection closed.")

    async def acquire(self) -> asyncpg.Connection:
        """
        Acquires a connection from the pool. This connection should be released
        back to the pool after use.

        Returns:
            asyncpg.Connection: An asynchronous PostgreSQL connection object.
        """
        if not self.pool:
            raise ConnectionError(
                "Database pool is not initialized. Call 'connect' first."
            )
        return await self.pool.acquire()

    async def release(self, conn: asyncpg.Connection):
        """
        Releases a connection back to the connection pool.

        Args:
            conn (asyncpg.Connection): The PostgreSQL connection to release.
        """
        if self.pool:
            await self.pool.release(conn)

    async def _execute(self, query: str, *args):
        """
        Internal method to execute an SQL query. It acquires a connection from
        the pool, executes the query, and releases the connection.

        Args:
            query (str): The SQL query to execute.
            *args: Positional arguments to be passed to the query.

        Returns:
            str: The status of the execution (e.g., 'INSERT 0 1').

        Raises:
            asyncpg.exceptions.PostgresError: If an error occurs during query execution.
        """
        async with self.pool.acquire() as conn:
            logger.debug(f"Executing SQL query: {query}, Arguments: {args}")
            try:
                return await conn.execute(query, *args)
            except asyncpg.exceptions.PostgresError as e:
                logger.error(f"SQL query error: {e}", exc_info=True)
                raise

    async def execute(self, query: str, *args):
        """
        Executes an SQL query.

        Args:
            query (str): The SQL query to execute.
            *args: Positional arguments to be passed to the query.

        Returns:
            str: The status of the execution (e.g., 'INSERT 0 1').

        Raises:
            asyncpg.exceptions.PostgresError: If an error occurs during query execution.
        """
        return await self._execute(query, *args)

    async def _fetch(self, query: str, *args) -> list[asyncpg.Record]:
        """
        Internal method to fetch all rows resulting from an SQL query. It
        acquires a connection from the pool, executes the query, fetches the
        results, and releases the connection.

        Args:
            query (str): The SQL query to execute.
            *args: Positional arguments to be passed to the query.

        Returns:
            list[asyncpg.Record]: A list of asyncpg.Record objects representing the fetched rows.

        Raises:
            asyncpg.exceptions.PostgresError: If an error occurs during query execution.
        """
        async with self.pool.acquire() as conn:
            logger.debug(f"Fetching data with query: {query}, Arguments: {args}")
            try:
                return await conn.fetch(query, *args)
            except asyncpg.exceptions.PostgresError as e:
                logger.error(f"SQL query error: {e}", exc_info=True)
                raise

    async def fetch(self, query: str, *args) -> list[asyncpg.Record]:
        """
        Fetches all rows resulting from an SQL query.

        Args:
            query (str): The SQL query to execute.
            *args: Positional arguments to be passed to the query.

        Returns:
            list[asyncpg.Record]: A list of asyncpg.Record objects representing the fetched rows.

        Raises:
            asyncpg.exceptions.PostgresError: If an error occurs during query execution.
        """
        return await self._fetch(query, *args)

    async def _fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """
        Internal method to fetch a single row resulting from an SQL query. It
        acquires a connection from the pool, executes the query, fetches the
        first row, and releases the connection.

        Args:
            query (str): The SQL query to execute.
            *args: Positional arguments to be passed to the query.

        Returns:
            Optional[asyncpg.Record]: An asyncpg.Record object representing the fetched row,
                                     or None if no rows were returned.

        Raises:
            asyncpg.exceptions.PostgresError: If an error occurs during query execution.
        """
        async with self.pool.acquire() as conn:
            logger.debug(f"Fetching one row with query: {query}, Arguments: {args}")
            try:
                return await conn.fetchrow(query, *args)
            except asyncpg.exceptions.PostgresError as e:
                logger.error(f"SQL query error: {e}", exc_info=True)
                raise

    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """
        Fetches a single row resulting from an SQL query.

        Args:
            query (str): The SQL query to execute.
            *args: Positional arguments to be passed to the query.

        Returns:
            Optional[asyncpg.Record]: An asyncpg.Record object representing the fetched row,
                                     or None if no rows were returned.

        Raises:
            asyncpg.exceptions.PostgresError: If an error occurs during query execution.
        """
        return await self._fetchrow(query, *args)
