import sqlite3

def search(year, method, host, facility):
    query = "SELECT DISTINCT pl_name, disc_year, discoverymethod, hostname, disc_facility FROM exoplanets WHERE 1=1"
    params = []
        
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
        
    try:
        conn = sqlite3.connect('exoplanets.db')
        c = conn.cursor()
        c.execute(query, params)
        results = c.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return []