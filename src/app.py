import os
import sqlite3
from flask import Flask, render_template, jsonify, request, send_from_directory
from src import database
from config import get_config

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Cargar configuración
cfg = get_config()
app.config.from_object(cfg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/api/stats')
def stats():
    user_id = request.args.get('user_id', app.config['DEFAULT_USER'])
    total, faltantes, repetidos = database.get_stats(user_id)
    
    return jsonify({
        'total': total,
        'faltantes': faltantes,
        'conseguidos': total - faltantes,
        'repetidos': repetidos,
        'porcentaje': round(((total - faltantes) / total) * 100, 1) if total > 0 else 0
    })

@app.route('/api/faltantes')
def faltantes():
    user_id = request.args.get('user_id', app.config['DEFAULT_USER'])
    rows = database.get_faltantes(user_id)
    data = {}
    for equipo, numero, nombre in rows:
        if equipo not in data:
            data[equipo] = []
        data[equipo].append(numero)
    return jsonify(data)

@app.route('/api/repetidos')
def repetidos():
    user_id = request.args.get('user_id', app.config['DEFAULT_USER'])
    rows = database.get_repetidos(user_id)
    data = {}
    for equipo, numero, cantidad in rows:
        if equipo not in data:
            data[equipo] = []
        data[equipo].append({'numero': numero, 'cantidad': cantidad})
    return jsonify(data)

@app.route('/api/album')
def album():
    user_id = request.args.get('user_id', app.config['DEFAULT_USER'])
    rows = database.get_all_cromos(user_id)
    
    data_by_equipo = {}
    for equipo, numero, cantidad, nombre in rows:
        if equipo not in data_by_equipo:
            data_by_equipo[equipo] = []
        data_by_equipo[equipo].append({'numero': numero, 'cantidad': cantidad, 'nombre': nombre})
            
    for eq in data_by_equipo:
        data_by_equipo[eq].sort(key=lambda x: x['numero'])
        
    fwc = data_by_equipo.get('FWC', [])
    data_by_equipo['FWC1'] = [c for c in fwc if c['numero'] <= 8]
    data_by_equipo['FWC2'] = [c for c in fwc if c['numero'] >= 9]
    if 'FWC' in data_by_equipo:
        del data_by_equipo['FWC']
        
    estructura = [
        {"nombre": "Especiales", "equipos": ["FWC1"]},
        {"nombre": "Grupo A", "equipos": ["MEX", "RSA", "KOR", "CZE"]},
        {"nombre": "Grupo B", "equipos": ["CAN", "BIH", "QAT", "SUI"]},
        {"nombre": "Grupo C", "equipos": ["BRA", "MAR", "HAI", "SCO"]},
        {"nombre": "Grupo D", "equipos": ["USA", "PAR", "AUS", "TUR"]},
        {"nombre": "Grupo E", "equipos": ["GER", "CUW", "CIV", "ECU"]},
        {"nombre": "Grupo F", "equipos": ["NED", "JPN", "SWE", "TUN"]},
        {"nombre": "Grupo G", "equipos": ["BEL", "EGY", "IRN", "NZL"]},
        {"nombre": "Grupo H", "equipos": ["ESP", "CPV", "KSA", "URU"]},
        {"nombre": "Grupo I", "equipos": ["FRA", "SEN", "IRQ", "NOR"]},
        {"nombre": "Grupo J", "equipos": ["ARG", "ALG", "AUT", "JOR"]},
        {"nombre": "Grupo K", "equipos": ["POR", "COD", "UZB", "COL"]},
        {"nombre": "Grupo L", "equipos": ["ENG", "CRO", "GHA", "PAN"]},
        {"nombre": "History", "equipos": ["FWC2"]}
    ]
        
    return jsonify({'estructura': estructura, 'cromos': data_by_equipo})

@app.route('/api/tengo', methods=['POST'])
def tengo():
    req = request.json
    ids = req.get('ids')
    user_id = req.get('user_id', app.config['DEFAULT_USER'])
    
    if not ids:
        return jsonify({'error': 'No IDs provided'}), 400
        
    cromos = [c.strip().upper() for c in ids.split(',') if c.strip()]
    for c_id in cromos:
        database.update_cromo(user_id, c_id, 1)
        
    return jsonify({'success': True, 'registrados': cromos})

@app.route('/api/quitar', methods=['POST'])
def quitar():
    req = request.json
    ids = req.get('ids')
    user_id = req.get('user_id', app.config['DEFAULT_USER'])
    
    if not ids:
        return jsonify({'error': 'No IDs provided'}), 400
        
    cromos = [c.strip().upper() for c in ids.split(',') if c.strip()]
    for c_id in cromos:
        database.update_cromo(user_id, c_id, -1)
        
    return jsonify({'success': True, 'quitados': cromos})

@app.route('/api/historial')
def historial():
    user_id = request.args.get('user_id', app.config['DEFAULT_USER'])
    rows = database.get_historial(user_id)
    return jsonify([{'cromo_id': r[0], 'accion': r[1], 'fecha': r[2]} for r in rows])

@app.route('/api/usuarios')
def usuarios():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT user_id FROM cromos')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([r[0] for r in rows])

@app.route('/api/update_name', methods=['POST'])
def update_name():
    req = request.json
    id_cromo = req.get('id')
    nombre = req.get('nombre')
    user_id = req.get('user_id', app.config['DEFAULT_USER'])
    
    if not id_cromo:
        return jsonify({'error': 'No ID provided'}), 400
        
    database.update_cromo_name(user_id, id_cromo, nombre)
    return jsonify({'success': True})

if __name__ == '__main__':
    # Inicializar BD
    database.init_db()
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
