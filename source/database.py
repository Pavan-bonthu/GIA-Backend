import pyodbc

def get_connection():
    return pyodbc.connect(
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=LAPTOP-S5LL24VA;"
        r"DATABASE=MainDB;"
        r"UID=sa;"
        r"PWD=20Kn1@05H8;"
    )

def fetch_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results
