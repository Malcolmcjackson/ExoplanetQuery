import requests
import sqlite3
import csv
from io import StringIO

# Function to create SQLite database and table
def create_database():
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

# Load exoplanet data from CSV into SQLite database
def load_exoplanet_data():
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
