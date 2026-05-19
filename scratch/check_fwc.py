import sqlite3
import os

DB_PATH = 'coleccion.db'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT id, numero, cantidad FROM cromos WHERE equipo = 'FWC' AND user_id = 'MarcosDB12' ORDER BY numero")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
