import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), 'coleccion.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def normalize_cromo_id(id_cromo):
    id_cromo = id_cromo.strip().upper()
    # Capturar equipo y número, permitiendo que el número sea 0 o 00
    match = re.match(r'^([A-Z]+)[-\s]*0*(\d+)$', id_cromo)
    if match:
        equipo = match.group(1)
        numero = int(match.group(2))
        return f"{equipo} {numero}"
    return id_cromo

def inicializar_album_completo(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM cromos WHERE user_id = ?', (user_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    secciones = {
        'FWC': 19,
        'MEX': 20, 'RSA': 20, 'KOR': 20, 'CZE': 20,
        'CAN': 20, 'BIH': 20, 'QAT': 20, 'SUI': 20,
        'BRA': 20, 'MAR': 20, 'HAI': 20, 'SCO': 20,
        'USA': 20, 'PAR': 20, 'AUS': 20, 'TUR': 20,
        'GER': 20, 'CUW': 20, 'CIV': 20, 'ECU': 20,
        'NED': 20, 'JPN': 20, 'SWE': 20, 'TUN': 20,
        'BEL': 20, 'EGY': 20, 'IRN': 20, 'NZL': 20,
        'ESP': 20, 'CPV': 20, 'KSA': 20, 'URU': 20,
        'FRA': 20, 'SEN': 20, 'IRQ': 20, 'NOR': 20,
        'ARG': 20, 'ALG': 20, 'AUT': 20, 'JOR': 20,
        'POR': 20, 'COD': 20, 'UZB': 20, 'COL': 20,
        'ENG': 20, 'CRO': 20, 'GHA': 20, 'PAN': 20
    }

    for equipo, cantidad in secciones.items():
        # FWC empieza en 0 (cromo 00)
        start = 0 if equipo == 'FWC' else 1
        for i in range(start, cantidad + 1):
            id_cromo = f"{equipo} {i}"
            cursor.execute('''
                INSERT INTO cromos (user_id, id, equipo, numero, nombre, cantidad)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, id_cromo, equipo, i, "", 0))
    
    conn.commit()
    conn.close()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cromos (
            user_id TEXT,
            id TEXT,
            equipo TEXT,
            numero INTEGER,
            nombre TEXT,
            cantidad INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            cromo_id TEXT,
            accion TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cromos_user_id ON cromos(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cromos_equipo ON cromos(equipo)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_historial_user ON historial(user_id)')
    conn.commit()
    conn.close()

def get_cromo(user_id, id_cromo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, cantidad FROM cromos WHERE user_id = ? AND id = ?', (user_id, id_cromo))
    row = cursor.fetchone()
    conn.close()
    return row

def update_cromo(user_id, id_cromo, cantidad, nombre=""):
    # Asegurar que la colección existe para este usuario
    inicializar_album_completo(user_id)
    
    conn = get_connection()
    cursor = conn.cursor()
    id_cromo = normalize_cromo_id(id_cromo)
    
    partes = id_cromo.split(" ")
    equipo = partes[0] if len(partes) > 0 else id_cromo
    numero = None
    if len(partes) > 1 and partes[1].isdigit():
        numero = int(partes[1])

    cursor.execute('''
        INSERT INTO cromos (user_id, id, equipo, numero, nombre, cantidad)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, id) DO UPDATE SET 
            cantidad = MAX(0, cromos.cantidad + excluded.cantidad),
            nombre = CASE WHEN excluded.nombre != '' THEN excluded.nombre ELSE cromos.nombre END
    ''', (user_id, id_cromo, equipo, numero, nombre, cantidad))
    
    accion = "añadido" if cantidad > 0 else "borrado"
    cursor.execute('''
        INSERT INTO historial (user_id, cromo_id, accion)
        VALUES (?, ?, ?)
    ''', (user_id, id_cromo, accion))

    conn.commit()
    conn.close()

def get_faltantes(user_id):
    inicializar_album_completo(user_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT equipo, numero, nombre FROM cromos WHERE user_id = ? AND cantidad = 0 ORDER BY equipo, numero', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_repetidos(user_id):
    inicializar_album_completo(user_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT equipo, numero, cantidad FROM cromos WHERE user_id = ? AND cantidad > 1 ORDER BY equipo, numero', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_cromos(user_id):
    inicializar_album_completo(user_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT equipo, numero, cantidad, nombre FROM cromos WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stats(user_id):
    inicializar_album_completo(user_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM cromos WHERE user_id = ?', (user_id,))
    total = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM cromos WHERE user_id = ? AND cantidad = 0', (user_id,))
    faltantes = cursor.fetchone()[0]
    cursor.execute('SELECT SUM(cantidad - 1) FROM cromos WHERE user_id = ? AND cantidad > 1', (user_id,))
    res_rep = cursor.fetchone()[0]
    repetidos = res_rep if res_rep else 0
    conn.close()
    return total, faltantes, repetidos

def get_historial(user_id, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT cromo_id, accion, fecha FROM historial WHERE user_id = ? ORDER BY fecha DESC LIMIT ?', (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows

def repair_user_collection(user_id):
    """Añade los cromos que falten en la colección de un usuario (como el FWC 0)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    secciones = {
        'FWC': 19, 'MEX': 20, 'RSA': 20, 'KOR': 20, 'CZE': 20,
        'CAN': 20, 'BIH': 20, 'QAT': 20, 'SUI': 20,
        'BRA': 20, 'MAR': 20, 'HAI': 20, 'SCO': 20,
        'USA': 20, 'PAR': 20, 'AUS': 20, 'TUR': 20,
        'GER': 20, 'CUW': 20, 'CIV': 20, 'ECU': 20,
        'NED': 20, 'JPN': 20, 'SWE': 20, 'TUN': 20,
        'BEL': 20, 'EGY': 20, 'IRN': 20, 'NZL': 20,
        'ESP': 20, 'CPV': 20, 'KSA': 20, 'URU': 20,
        'FRA': 20, 'SEN': 20, 'IRQ': 20, 'NOR': 20,
        'ARG': 20, 'ALG': 20, 'AUT': 20, 'JOR': 20,
        'POR': 20, 'COD': 20, 'UZB': 20, 'COL': 20,
        'ENG': 20, 'CRO': 20, 'GHA': 20, 'PAN': 20
    }

    for equipo, cantidad in secciones.items():
        start = 0 if equipo == 'FWC' else 1
        for i in range(start, cantidad + 1):
            id_cromo = f"{equipo} {i}"
            cursor.execute('''
                INSERT OR IGNORE INTO cromos (user_id, id, equipo, numero, nombre, cantidad)
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (user_id, id_cromo, equipo, i, ""))
            
    conn.commit()
    conn.close()

def update_cromo_name(user_id, id_cromo, nombre):
    conn = get_connection()
    cursor = conn.cursor()
    id_cromo = normalize_cromo_id(id_cromo)
    cursor.execute('''
        UPDATE cromos SET nombre = ? WHERE user_id = ? AND id = ?
    ''', (nombre, user_id, id_cromo))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("Inicializando base de datos...")
    init_db()
    print("Base de datos inicializada en:", DB_PATH)
