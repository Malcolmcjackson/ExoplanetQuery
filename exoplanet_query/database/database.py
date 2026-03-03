import sqlite3
import pandas as pd

class Database:
    """
    Lightweight database helper for optional SQLite storage of exoplanet data.
    
    In the Streamlit version of the app, DataFrames are the primary data structure
    for filtering and visualization, but SQLite can still be used for persistence
    or advanced querying outside the UI.
    """

    def __init__(self, db_name='exoplanets.db'):
        """
        Initialize the database helper with a target SQLite file.
        """
        self.db_name = db_name

    # ------------------------------------------------------------------
    # 💫 1. Connection Helper
    # ------------------------------------------------------------------
    def connect(self):
        """Return a new SQLite connection."""
        return sqlite3.connect(self.db_name)

    # ------------------------------------------------------------------
    # 💫 2. Execute a SQL query (generic helper)
    # ------------------------------------------------------------------
    def execute_query(self, query, params=None, return_df=False):
        """
        Execute a SQL query and optionally return a pandas DataFrame.

        Args:
            query (str): SQL query string.
            params (tuple): Optional query parameters.
            return_df (bool): Whether to return a pandas DataFrame.

        Returns:
            list | pandas.DataFrame: Query results.
        """
        conn = self.connect()

        if return_df:
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            return df

        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        conn.close()
        return results

    # ------------------------------------------------------------------
    # 💫 3. Fetch DISTINCT column values (helper for dropdowns)
    # ------------------------------------------------------------------
    def get_distinct_values(self, column):
        """
        Return a sorted list of unique values in a given column.
        Perfect for populating Streamlit filters.
        """
        query = f"SELECT DISTINCT {column} FROM exoplanets ORDER BY {column}"
        rows = self.execute_query(query)
        return [row[0] for row in rows]

    # ------------------------------------------------------------------
    # 💫 4. Return FULL TABLE as a DataFrame
    # ------------------------------------------------------------------
    def get_full_table(self):
        """
        Return the entire exoplanets table as a pandas DataFrame.
        Useful if the app chooses to query SQLite instead of DataFrame.
        """
        query = "SELECT * FROM exoplanets"
        return self.execute_query(query, return_df=True)

    # ------------------------------------------------------------------
    # 💫 5. Query by filters (DataFrame style, but SQL-backed)
    # ------------------------------------------------------------------
    def query_exoplanets(
        self,
        name=None,
        year=None,
        method=None,
        host=None,
        facility=None
    ):
        """
        Perform a dynamic filtered query on the SQLite database.
        Streamlit will typically use DataFrame filtering instead,
        but this remains available for compatibility.
        """
        base = "SELECT * FROM exoplanets WHERE 1=1"
        params = []

        if name:
            base += " AND pl_name LIKE ?"
            params.append(f"%{name}%")
        if year:
            base += " AND disc_year = ?"
            params.append(year)
        if method:
            base += " AND discoverymethod = ?"
            params.append(method)
        if host:
            base += " AND hostname LIKE ?"
            params.append(f"%{host}%")
        if facility:
            base += " AND disc_facility = ?"
            params.append(facility)

        return self.execute_query(base, params=params, return_df=True)