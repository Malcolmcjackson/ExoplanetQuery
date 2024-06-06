from database.database import Database

class ExoplanetModel:
    """
    Model class for handling exoplanet data.

    This class interacts with the database to retrieve distinct values and search for exoplanets based on user queries.

    Public Methods:
        - __init__: Initialize the model.
        - get_distinct_names: Get distinct planet names from the database.
        - get_distinct_years: Get distinct years of discovery from the database.
        - get_distinct_methods: Get distinct discovery methods from the database.
        - get_distinct_hosts: Get distinct host names from the database.
        - get_distinct_facilities: Get distinct discovery facilities from the database.
        - search_exoplanets: Search for exoplanets based on specified criteria.

    Attributes:
        db (Database): An instance of the Database class used for database interaction.
    """
    def __init__(self):
        self.db = Database()

    def get_distinct_names(self):
        """
        Get distinct planet names from the database.

        Returns:
            list: A list of distinct planet names.
        """
        return self.db.get_distinct_values('pl_name')

    def get_distinct_years(self):
        """
        Get distinct years of discovery from the database.

        Returns:
            list: A list of distinct years of discovery.
        """
        years = self.db.get_distinct_values('disc_year')
        return [str(year) for year in years]

    def get_distinct_methods(self):
        """
        Get distinct discovery methods from the database.

        Returns:
            list: A list of distinct discovery methods.
        """
        return self.db.get_distinct_values('discoverymethod')

    def get_distinct_hosts(self):
        """
        Get distinct host names from the database.

        Returns:
            list: A list of distinct host names.
        """
        return self.db.get_distinct_values('hostname')

    def get_distinct_facilities(self):
        """
        Get distinct discovery facilities from the database.

        Returns:
            list: A list of distinct discovery facilities.
        """
        return self.db.get_distinct_values('disc_facility')

    def search_exoplanets(self, name, year, method, host, facility):
        """
        Search for exoplanets based on specified criteria.

        Args:
            name (str): The name of the exoplanet.
            year (str): The year of discovery.
            method (str): The discovery method.
            host (str): The name of the host.
            facility (str): The name of the discovery facility.

        Returns:
            list: A list of tuples representing the search results.
        """
        query = "SELECT pl_name, disc_year, discoverymethod, hostname, disc_facility FROM exoplanets WHERE 1=1"
        params = []

        if name:
            query += " AND pl_name = ?"
            params.append(name)
        if year:
            query += " AND disc_year = ?"
            params.append(year)
        if method:
            query += " AND discoverymethod = ?"
            params.append(method)
        if host:
            query += " AND hostname = ?"
            params.append(host)
        if facility:
            query += " AND disc_facility = ?"
            params.append(facility)

        return self.db.execute_query(query, params)