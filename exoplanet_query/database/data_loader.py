import requests
import sqlite3
import csv
from io import StringIO

def create_database():
    """
    Create the exoplanets SQLite database and the 'exoplanets' table.

    This function creates a new SQLite database named 'exoplanets.db' if it does not
    already exist and sets up a table for storing exoplanet data. The table includes
    columns for planet name, discovery year, discovery method, host name, discovery
    facility, distance from Earth, radius, mass, orbital period, star radius, and
    equilibrium temperature.
    """
    conn = sqlite3.connect('exoplanets.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS exoplanets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pl_name TEXT,
            disc_year INTEGER,
            discoverymethod TEXT,
            hostname TEXT,
            disc_facility TEXT,
            sy_dist REAL,
            pl_rade REAL,
            pl_masse REAL,
            pl_orbper REAL,
            st_rad REAL,
            pl_eqt REAL
        )
    ''')
    conn.commit()
    conn.close()

def load_exoplanet_data():
    """
    Load exoplanet data from the NASA Exoplanet Archive into the SQLite database.

    This function sends a request to the NASA Exoplanet Archive's TAP service to
    retrieve exoplanet data in CSV format. The retrieved data is then parsed and
    inserted into the 'exoplanets' table in the SQLite database.

    If the data retrieval or insertion process encounters any errors, an exception
    message will be printed to the console.
    """
    # Base URL for the TAP service
    base_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"

    # Construct the TAP query to select specific columns from the 'ps' table
    query = "select pl_name, disc_year, discoverymethod, hostname, disc_facility, sy_dist, pl_rade, pl_masse, pl_orbper, st_rad, pl_eqt from ps"

    # Construct the full URL with the query and format set to CSV
    url = f"{base_url}query={query}&format=csv"

    try:
        # Send GET request to the TAP service
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        csv_data = response.text  # Get the CSV data
        
        # Read CSV data and insert into SQLite database
        conn = sqlite3.connect('exoplanets.db')
        c = conn.cursor()
        reader = csv.reader(StringIO(csv_data))
        next(reader)  # Skip header row
        for row in reader:
            c.execute('''
                INSERT INTO exoplanets 
                      (pl_name, disc_year, discoverymethod, hostname, disc_facility, 
                      sy_dist, pl_rade, pl_masse, pl_orbper, st_rad, pl_eqt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row)
        conn.commit()
        conn.close()
    except requests.RequestException as e:
        print("Error loading exoplanet data:", e)
