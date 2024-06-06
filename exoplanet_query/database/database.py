import sqlite3

class Database:
    """
    Database class for interacting with the exoplanets database.

    This class provides methods to connect to the database, execute queries, and retrieve distinct values from specified columns.

    Public Methods:
        - __init__: Initialize the database with the specified database name.
        - connect: Connect to the database.
        - execute_query: Execute the provided SQL query with optional parameters.
        - get_distinct_values: Get distinct values from the specified column in the exoplanets table.

    Attributes:
        db_name (str): The name of the exoplanets database.
    """
    def __init__(self, db_name='exoplanets.db'):
        """
        Initialize the database with the specified database name.

        Args:
            db_name (str): The name of the exoplanets database.
        """
        self.db_name = db_name

    def connect(self):
        """
        Connect to the database.

        Returns:
            sqlite3.Connection: A connection object to the exoplanets database.
        """
        return sqlite3.connect(self.db_name)

    def execute_query(self, query, params=None):
        """
        Execute the provided SQL query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to substitute in the query (default is None).

        Returns:
            list: A list of tuples representing the query results.
        """
        conn = self.connect()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    def get_distinct_values(self, column):
        """
        Get distinct values from the specified column in the exoplanets table.

        Args:
            column (str): The column name from which to retrieve distinct values.

        Returns:
            list: A list of distinct values from the specified column.
        """
        query = f"SELECT DISTINCT {column} FROM exoplanets ORDER BY {column} ASC"
        return [row[0] for row in self.execute_query(query)]
