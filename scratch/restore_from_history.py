import database
import re
import os

def restore():
    user_id = 'MarcosDB12'
    history_file = os.path.join(os.path.dirname(__file__), 'history_dump.txt')
    
    if not os.path.exists(history_file):
        print("Error: No se encontró history_dump.txt")
        return
        
    print("Iniciando restauración desde el historial...")
    
    # 1. Asegurar que la colección esté limpia y lista para el usuario
    database.repair_user_collection(user_id)
    
    # Limpiar el historial actual en base de datos para no duplicar entradas
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM historial WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE cromos SET cantidad = 0 WHERE user_id = ?', (user_id,))
    conn.commit()
    
    # Leer el dump
    with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    # Las líneas están en orden cronológico inverso (el más reciente arriba),
    # así que para restaurar el estado de la colección y mantener el orden del historial,
    # debemos procesar de abajo hacia arriba (orden cronológico directo).
    lines.reverse()
    
    restored_actions = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Parsear formato: ('SWE 13', 'añadido', '2026-05-15 06:33:19')
        match = re.match(r"\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*\)", line)
        if match:
            cromo_id = match.group(1).strip()
            accion = match.group(2).strip()
            fecha = match.group(3).strip()
            
            # Limpiar nombre de acción
            if 'adido' in accion or 'a' in accion or '1' in accion:
                accion = 'añadido'
            else:
                accion = 'borrado'
                
            delta = 1 if accion == 'añadido' else -1
            
            # Registrar el cambio en la base de datos
            c_match = re.match(r"^([A-Z0-9]+)\s*(\d+)$", cromo_id)
            if c_match:
                equipo = c_match.group(1)
                numero = int(c_match.group(2))
                
                # Actualizar cantidad de cromos
                cursor.execute('''
                    UPDATE cromos 
                    SET cantidad = MAX(0, cantidad + ?) 
                    WHERE user_id = ? AND equipo = ? AND numero = ?
                ''', (delta, user_id, equipo, numero))
                
                # Registrar en historial con su fecha original
                cursor.execute('''
                    INSERT INTO historial (user_id, cromo_id, accion, fecha)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, cromo_id, accion, fecha))
                
                restored_actions += 1
                
    conn.commit()
    conn.close()
    print(f"Restauración completa. Se procesaron {restored_actions} acciones de historial.")

if __name__ == '__main__':
    restore()
