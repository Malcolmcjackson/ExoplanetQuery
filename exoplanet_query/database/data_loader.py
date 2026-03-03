import requests
import pandas as pd
from io import StringIO

# -------------------------------------------------------------------
# 🌟 1. OPTIONAL: Create SQLite DB (not required for Streamlit)
# -------------------------------------------------------------------
# def create_database():
#     """
#     Create the exoplanets SQLite database and the 'exoplanets' table.

#     Streamlit apps normally work directly with DataFrames,
#     but SQLite can still be used for persistence if desired.
#     """
#     conn = sqlite3.connect('exoplanets.db')
#     c = conn.cursor()

#     c.execute('''
#         CREATE TABLE IF NOT EXISTS exoplanets (
#             pl_name TEXT,
#             disc_year INTEGER,
#             discoverymethod TEXT,
#             hostname TEXT,
#             disc_facility TEXT,
#             sy_dist REAL,
#             pl_rade REAL,
#             pl_masse REAL,
#             pl_orbper REAL,
#             st_rad REAL,
#             pl_eqt REAL
#         )
#     ''')

#     conn.commit()
#     conn.close()


# -------------------------------------------------------------------
# 🌟 2. Fetch NASA Exoplanet CSV → return a DataFrame
# -------------------------------------------------------------------
def fetch_exoplanet_csv():
    """
    Fetch exoplanet data from NASA's Exoplanet Archive in CSV format,
    returning a pandas DataFrame.

    This is the core data-loading function used by Streamlit.
    """
    base_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
    query = (
        "select pl_name, disc_year, discoverymethod, hostname, disc_facility, "
        "sy_dist, pl_rade, pl_masse, pl_orbper, st_rad, pl_eqt from ps"
    )

    url = f"{base_url}query={query}&format=csv"

    response = requests.get(url)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))

    return df


# # -------------------------------------------------------------------
# # 🌟 3. Optional: Save DataFrame → SQLite DB
# # -------------------------------------------------------------------
# def load_dataframe_into_db(df):
#     """
#     Insert the exoplanet DataFrame into SQLite (optional).

#     Streamlit does not need SQLite for filtering, but this preserves
#     compatibility with your pre-existing Database class.
#     """
#     conn = sqlite3.connect("exoplanets.db")
#     df.to_sql("exoplanets", conn, if_exists="replace", index=False)
#     conn.close()


# -------------------------------------------------------------------
# 🌟 4. One unified function for Streamlit
# -------------------------------------------------------------------
def get_exoplanet_data(save_to_db=False):
    """
    Streamlit-friendly high-level loader:
    - Fetch the CSV
    - Return a tidy DataFrame
    - Optionally store it in SQLite for external use

    Args:
        save_to_db (bool): Whether to write the data to SQLite

    Returns:
        pandas.DataFrame: Exoplanet dataset
    """
    df = fetch_exoplanet_csv()

    if save_to_db:
        create_database()
        load_dataframe_into_db(df)

    return df