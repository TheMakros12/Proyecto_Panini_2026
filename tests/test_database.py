import pytest
import sqlite3
import os
import tempfile
from src import database
from config import Config


@pytest.fixture
def temp_db():
    """Crear base de datos temporal para las pruebas"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Temporalmente cambiar la ruta de la BD
    original_path = database.DB_PATH
    database.DB_PATH = path
    Config.DATABASE_PATH = path
    
    # Inicializar la BD
    database.init_db()
    
    yield path
    
    # Limpiar
    database.DB_PATH = original_path
    Config.DATABASE_PATH = original_path
    os.unlink(path)


class TestDatabaseConnection:
    def test_get_connection(self, temp_db):
        """Verificar que se puede obtener conexión a la base de datos"""
        conn = database.get_connection()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_init_db_creates_tables(self, temp_db):
        """Verificar que init_db crea las tablas necesarias"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Verificar tabla cromos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cromos'")
        assert cursor.fetchone() is not None
        
        # Verificar tabla historial
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='historial'")
        assert cursor.fetchone() is not None
        
        conn.close()


class TestNormalization:
    def test_normalize_cromo_id_basic(self):
        """Probar normalización básica de ID de cromo"""
        assert database.normalize_cromo_id('esp 1') == 'ESP 1'
        assert database.normalize_cromo_id('ESP 1') == 'ESP 1'
        assert database.normalize_cromo_id('arg 5') == 'ARG 5'
    
    def test_normalize_cromo_id_with_hyphen(self):
        """Probar normalización con guión"""
        assert database.normalize_cromo_id('esp-1') == 'ESP 1'
        assert database.normalize_cromo_id('ESP-5') == 'ESP 5'
    
    def test_normalize_cromo_id_with_leading_zeros(self):
        """Probar normalización con ceros al inicio"""
        assert database.normalize_cromo_id('ESP 001') == 'ESP 1'
        assert database.normalize_cromo_id('ARG 05') == 'ARG 5'
        assert database.normalize_cromo_id('FWC 00') == 'FWC 0'


class TestAlbumInitialization:
    def test_inicializar_album_completo(self, temp_db):
        """Verificar que se inicializa el álbum completo"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM cromos WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        # Total esperado: FWC(19) + 32 equipos * 20 = 659 cromos
        assert count == 659
    
    def test_no_duplicate_album_init(self, temp_db):
        """Verificar que no se duplica al inicializar dos veces"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.inicializar_album_completo(user_id)
        
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM cromos WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        assert count == 659


class TestCromoOperations:
    def test_update_cromo_add(self, temp_db):
        """Probar añadir un cromo"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo is not None
        assert cromo[2] == 1  # cantidad
    
    def test_update_cromo_remove(self, temp_db):
        """Probar remover un cromo"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 1', -1)
        
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo[2] == 0  # cantidad debe ser 0
    
    def test_update_cromo_multiple(self, temp_db):
        """Probar añadir múltiples veces el mismo cromo"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 1', 1)
        
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo[2] == 3  # cantidad debe ser 3
    
    def test_update_cromo_prevents_negative(self, temp_db):
        """Probar que cantidad nunca es negativa"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', -5)  # Intentar cantidad negativa
        
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo[2] == 0  # cantidad debe ser 0 (mínimo)
    
    def test_update_cromo_with_name(self, temp_db):
        """Probar actualizar nombre del cromo"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1, 'Iker Casillas')
        
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo[1] == 'Iker Casillas'


class TestStatistics:
    def test_get_stats_empty(self, temp_db):
        """Probar estadísticas con álbum vacío"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        total, faltantes, repetidos = database.get_stats(user_id)
        assert total == 659
        assert faltantes == 659
        assert repetidos == 0
    
    def test_get_stats_with_cromos(self, temp_db):
        """Probar estadísticas con cromos añadidos"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 2', 1)
        database.update_cromo(user_id, 'ESP 3', 2)  # Repetido
        
        total, faltantes, repetidos = database.get_stats(user_id)
        assert total == 659
        assert faltantes == 657  # 659 - 3 + 1 (por el repetido que cuenta como 1)
        assert repetidos == 1  # 2 - 1 = 1 extra


class TestMissingAndDuplicate:
    def test_get_faltantes(self, temp_db):
        """Probar obtener cromos faltantes"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 2', 1)
        
        faltantes = database.get_faltantes(user_id)
        assert len(faltantes) == 657  # 659 - 2
        
        # Verificar que ESP 1 y ESP 2 no están en faltantes
        faltantes_ids = [(e, n) for e, n, _ in faltantes]
        assert ('ESP', 1) not in faltantes_ids
        assert ('ESP', 2) not in faltantes_ids
    
    def test_get_repetidos(self, temp_db):
        """Probar obtener cromos repetidos"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 2)
        database.update_cromo(user_id, 'ESP 2', 3)
        database.update_cromo(user_id, 'ARG 1', 1)  # No repetido
        
        repetidos = database.get_repetidos(user_id)
        assert len(repetidos) == 2
        
        repetidos_dict = {(e, n): c for e, n, c in repetidos}
        assert repetidos_dict[('ESP', 1)] == 2
        assert repetidos_dict[('ESP', 2)] == 3


class TestAllCromos:
    def test_get_all_cromos(self, temp_db):
        """Probar obtener todos los cromos"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        cromos = database.get_all_cromos(user_id)
        assert len(cromos) == 659


class TestHistory:
    def test_get_historial_empty(self, temp_db):
        """Probar historial vacío"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        historial = database.get_historial(user_id)
        assert len(historial) == 0
    
    def test_get_historial_with_actions(self, temp_db):
        """Probar historial con acciones"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 2', 1)
        database.update_cromo(user_id, 'ESP 1', -1)
        
        historial = database.get_historial(user_id, limit=10)
        assert len(historial) == 3
        
        # El último debe ser "borrado"
        assert historial[0][1] == 'borrado'
        # Los anteriores deben ser "añadido"
        assert historial[1][1] == 'añadido'
        assert historial[2][1] == 'añadido'
    
    def test_get_historial_limit(self, temp_db):
        """Probar límite de historial"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        for i in range(1, 21):
            database.update_cromo(user_id, f'ESP {i}', 1)
        
        historial = database.get_historial(user_id, limit=5)
        assert len(historial) == 5


class TestUserCollection:
    def test_repair_user_collection(self, temp_db):
        """Probar reparar colección de usuario"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cromos WHERE user_id = ? AND equipo = ?', (user_id, 'ESP'))
        conn.commit()
        conn.close()
        
        # Verificar que faltan los de ESP
        cromos_antes = database.get_all_cromos(user_id)
        assert len(cromos_antes) == 639  # 659 - 20 (ESP)
        
        # Reparar
        database.repair_user_collection(user_id)
        
        cromos_despues = database.get_all_cromos(user_id)
        assert len(cromos_despues) == 659


class TestUpdateCromoName:
    def test_update_cromo_name(self, temp_db):
        """Probar actualizar nombre de cromo"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        database.update_cromo_name(user_id, 'ESP 1', 'Iker Casillas')
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo[1] == 'Iker Casillas'
    
    def test_update_cromo_name_with_normalization(self, temp_db):
        """Probar actualizar nombre con normalización de ID"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        database.update_cromo_name(user_id, 'esp 1', 'Iker Casillas')
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo[1] == 'Iker Casillas'
