import pytest
import json
import tempfile
import os
from src.app import app
from src import database
from config import Config


@pytest.fixture
def temp_db():
    """Crear base de datos temporal para las pruebas"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    original_path = database.DB_PATH
    database.DB_PATH = path
    Config.DATABASE_PATH = path
    
    database.init_db()
    
    yield path
    
    database.DB_PATH = original_path
    Config.DATABASE_PATH = original_path
    os.unlink(path)


@pytest.fixture
def client(temp_db):
    """Crear cliente de prueba de Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestIndexRoute:
    def test_index_returns_200(self, client):
        """Verificar que la ruta raíz devuelve 200"""
        response = client.get('/')
        assert response.status_code == 200


class TestStatsRoute:
    def test_stats_empty_album(self, client):
        """Probar stats con álbum vacío"""
        database.inicializar_album_completo(Config.DEFAULT_USER)
        response = client.get('/api/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['total'] == 659
        assert data['faltantes'] == 659
        assert data['conseguidos'] == 0
        assert data['repetidos'] == 0
        assert data['porcentaje'] == 0
    
    def test_stats_with_cromos(self, client):
        """Probar stats con cromos añadidos"""
        user_id = Config.DEFAULT_USER
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 2', 2)
        
        response = client.get('/api/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['total'] == 659
        assert data['conseguidos'] == 2
        assert data['faltantes'] == 657
    
    def test_stats_with_custom_user(self, client):
        """Probar stats con usuario personalizado"""
        user_id = 'custom_user'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ARG 1', 1)
        
        response = client.get(f'/api/stats?user_id={user_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['conseguidos'] == 1


class TestFaltantesRoute:
    def test_faltantes_empty(self, client):
        """Probar faltantes con álbum vacío"""
        database.inicializar_album_completo(Config.DEFAULT_USER)
        response = client.get('/api/faltantes')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Todos los equipos deben estar presentes con todos sus cromos
        assert 'ESP' in data
        assert len(data['ESP']) == 20
    
    def test_faltantes_with_cromos(self, client):
        """Probar faltantes después de añadir cromos"""
        user_id = Config.DEFAULT_USER
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 2', 1)
        
        response = client.get('/api/faltantes')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'ESP' in data
        assert len(data['ESP']) == 18  # 20 - 2


class TestRepetidosRoute:
    def test_repetidos_empty(self, client):
        """Probar repetidos con álbum vacío"""
        database.inicializar_album_completo(Config.DEFAULT_USER)
        response = client.get('/api/repetidos')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {}
    
    def test_repetidos_with_duplicates(self, client):
        """Probar repetidos con cromos duplicados"""
        user_id = Config.DEFAULT_USER
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 2)
        database.update_cromo(user_id, 'ARG 1', 3)
        
        response = client.get('/api/repetidos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'ESP' in data
        assert 'ARG' in data
        
        esp_data = data['ESP']
        assert len(esp_data) == 1
        assert esp_data[0]['numero'] == 1
        assert esp_data[0]['cantidad'] == 2


class TestAlbumRoute:
    def test_album_structure(self, client):
        """Probar estructura del álbum"""
        database.inicializar_album_completo(Config.DEFAULT_USER)
        response = client.get('/api/album')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'estructura' in data
        assert 'cromos' in data
        
        estructura = data['estructura']
        assert len(estructura) > 0
        assert estructura[0]['nombre'] == 'Especiales'
    
    def test_album_fwc_split(self, client):
        """Probar que FWC se divide en FWC1 y FWC2"""
        database.inicializar_album_completo(Config.DEFAULT_USER)
        response = client.get('/api/album')
        
        data = json.loads(response.data)
        cromos = data['cromos']
        
        assert 'FWC1' in cromos
        assert 'FWC2' in cromos
        assert 'FWC' not in cromos


class TestTengoRoute:
    def test_tengo_single_cromo(self, client):
        """Probar registrar un único cromo"""
        database.inicializar_album_completo(Config.DEFAULT_USER)
        
        response = client.post('/api/tengo', 
            json={'ids': 'ESP 1'},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'ESP 1' in data['registrados']
    
    def test_tengo_multiple_cromos(self, client):
        """Probar registrar múltiples cromos"""
        database.inicializar_album_completo(Config.DEFAULT_USER)
        
        response = client.post('/api/tengo',
            json={'ids': 'ESP 1, ARG 5, BRA 10'},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['registrados']) == 3
    
    def test_tengo_no_ids(self, client):
        """Probar error cuando no se proporcionan IDs"""
        response = client.post('/api/tengo',
            json={'ids': ''},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_tengo_custom_user(self, client):
        """Probar registrar cromo para usuario personalizado"""
        user_id = 'custom_user'
        database.inicializar_album_completo(user_id)
        
        response = client.post('/api/tengo',
            json={'ids': 'ESP 1', 'user_id': user_id},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo[2] == 1


class TestQuitarRoute:
    def test_quitar_cromo(self, client):
        """Probar quitar un cromo"""
        user_id = Config.DEFAULT_USER
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        
        response = client.post('/api/quitar',
            json={'ids': 'ESP 1'},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo[2] == 0
    
    def test_quitar_no_ids(self, client):
        """Probar error cuando no se proporcionan IDs"""
        response = client.post('/api/quitar',
            json={'ids': ''},
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestHistorialRoute:
    def test_historial_empty(self, client):
        """Probar historial vacío"""
        database.inicializar_album_completo(Config.DEFAULT_USER)
        
        response = client.get('/api/historial')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data == []
    
    def test_historial_with_actions(self, client):
        """Probar historial con acciones"""
        user_id = Config.DEFAULT_USER
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 2', 1)
        
        response = client.get('/api/historial')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) > 0
        assert data[0]['accion'] in ['añadido', 'borrado']


class TestUsuariosRoute:
    def test_usuarios_list(self, client):
        """Probar obtener lista de usuarios"""
        database.inicializar_album_completo('user1')
        database.inicializar_album_completo('user2')
        
        response = client.get('/api/usuarios')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'user1' in data
        assert 'user2' in data


class TestUpdateNameRoute:
    def test_update_name_success(self, client):
        """Probar actualizar nombre de cromo"""
        user_id = Config.DEFAULT_USER
        database.inicializar_album_completo(user_id)
        
        response = client.post('/api/update_name',
            json={'id': 'ESP 1', 'nombre': 'Iker Casillas'},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        
        cromo = database.get_cromo(user_id, 'ESP 1')
        assert cromo[1] == 'Iker Casillas'
    
    def test_update_name_no_id(self, client):
        """Probar error cuando no se proporciona ID"""
        response = client.post('/api/update_name',
            json={'nombre': 'Test'},
            content_type='application/json'
        )
        
        assert response.status_code == 400
