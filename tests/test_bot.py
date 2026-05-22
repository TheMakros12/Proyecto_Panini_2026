import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.bot import (
    format_ranges, get_user_id, estadisticas_logic, 
    falta_logic, repetidos_logic, web_logic
)
from src import database
from config import Config
import tempfile
import os


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


class TestFormatRanges:
    def test_empty_list(self):
        """Probar con lista vacía"""
        assert format_ranges([]) == ""
    
    def test_single_number(self):
        """Probar con un solo número"""
        assert format_ranges([5]) == "5"
    
    def test_consecutive_numbers(self):
        """Probar con números consecutivos"""
        assert format_ranges([1, 2, 3]) == "1-3"
        assert format_ranges([5, 6, 7, 8]) == "5-8"
    
    def test_mixed_numbers(self):
        """Probar con números mixtos (consecutivos y separados)"""
        assert format_ranges([1, 2, 3, 5]) == "1-3, 5"
        assert format_ranges([1, 2, 5, 6, 7, 10]) == "1-2, 5-7, 10"
    
    def test_unsorted_numbers(self):
        """Probar que se ordena antes de procesar"""
        assert format_ranges([5, 1, 3, 2]) == "1-3, 5"
        assert format_ranges([10, 5, 20, 15]) == "5, 10, 15, 20"
    
    def test_duplicates(self):
        """Probar con números duplicados"""
        assert format_ranges([1, 1, 2, 2, 3]) == "1-3"


class TestGetUserId:
    def test_default_user(self):
        """Probar que retorna el usuario por defecto"""
        mock_update = MagicMock()
        mock_update.effective_user = MagicMock()
        
        user_id = get_user_id(mock_update)
        assert user_id == Config.DEFAULT_USER


class TestEstadisticasLogic:
    @pytest.mark.asyncio
    async def test_estadisticas_logic_empty(self, temp_db):
        """Probar lógica de estadísticas con álbum vacío"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        reply_calls = []
        async def mock_reply(text, parse_mode=None):
            reply_calls.append(text)
        
        await estadisticas_logic(user_id, mock_reply)
        
        assert len(reply_calls) == 1
        text = reply_calls[0]
        assert 'Estadísticas' in text
        assert '0 / 659' in text or '0%' in text
    
    @pytest.mark.asyncio
    async def test_estadisticas_logic_with_cromos(self, temp_db):
        """Probar lógica de estadísticas con cromos"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 2', 1)
        database.update_cromo(user_id, 'ESP 3', 2)
        
        reply_calls = []
        async def mock_reply(text, parse_mode=None):
            reply_calls.append(text)
        
        await estadisticas_logic(user_id, mock_reply)
        
        assert len(reply_calls) == 1
        text = reply_calls[0]
        assert 'Estadísticas' in text
        assert '3' in text  # 3 conseguidos


class TestFaltaLogic:
    @pytest.mark.asyncio
    async def test_falta_logic_empty(self, temp_db):
        """Probar lógica de faltantes con álbum vacío"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        reply_calls = []
        async def mock_reply(text, parse_mode=None):
            reply_calls.append(text)
        
        await falta_logic(user_id, mock_reply)
        
        assert len(reply_calls) == 1
        text = reply_calls[0]
        assert 'Te faltan' in text
        assert '659' in text
    
    @pytest.mark.asyncio
    async def test_falta_logic_with_cromos(self, temp_db):
        """Probar lógica de faltantes después de añadir cromos"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 2', 1)
        database.update_cromo(user_id, 'ESP 3', 1)
        
        reply_calls = []
        async def mock_reply(text, parse_mode=None):
            reply_calls.append(text)
        
        await falta_logic(user_id, mock_reply)
        
        assert len(reply_calls) == 1
        text = reply_calls[0]
        assert 'Te faltan' in text
        assert '656' in text  # 659 - 3
    
    @pytest.mark.asyncio
    async def test_falta_logic_complete_team(self, temp_db):
        """Probar que muestra rangos de faltantes"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        # Añadir todos menos algunos
        for i in range(1, 19):
            database.update_cromo(user_id, f'ESP {i}', 1)
        
        reply_calls = []
        async def mock_reply(text, parse_mode=None):
            reply_calls.append(text)
        
        await falta_logic(user_id, mock_reply)
        
        assert len(reply_calls) == 1
        text = reply_calls[0]
        assert 'ESP' in text
        assert '19-20' in text or '19, 20' in text


class TestRepetidosLogic:
    @pytest.mark.asyncio
    async def test_repetidos_logic_empty(self, temp_db):
        """Probar lógica de repetidos con álbum sin duplicados"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        reply_calls = []
        async def mock_reply(text, parse_mode=None):
            reply_calls.append(text)
        
        await repetidos_logic(user_id, mock_reply)
        
        assert len(reply_calls) == 1
        text = reply_calls[0]
        assert 'No tienes' in text or 'no tienes' in text
    
    @pytest.mark.asyncio
    async def test_repetidos_logic_with_duplicates(self, temp_db):
        """Probar lógica de repetidos con cromos duplicados"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        database.update_cromo(user_id, 'ESP 1', 2)
        database.update_cromo(user_id, 'ESP 2', 3)
        database.update_cromo(user_id, 'ARG 1', 1)  # No repetido
        
        reply_calls = []
        async def mock_reply(text, parse_mode=None):
            reply_calls.append(text)
        
        await repetidos_logic(user_id, mock_reply)
        
        assert len(reply_calls) == 1
        text = reply_calls[0]
        assert 'Cromos repetidos' in text
        assert 'ESP' in text
        assert '2' in text or 'x' in text  # Formato del duplicado


class TestWebLogic:
    @pytest.mark.asyncio
    async def test_web_logic(self, temp_db):
        """Probar lógica de enlace web"""
        reply_calls = []
        async def mock_reply(text, parse_mode=None):
            reply_calls.append(text)
        
        await web_logic(mock_reply)
        
        assert len(reply_calls) == 1
        text = reply_calls[0]
        assert 'Dashboard' in text or 'dashboard' in text
        assert Config.WEB_URL in text


class TestBotIntegration:
    @pytest.mark.asyncio
    async def test_command_flow(self, temp_db):
        """Probar flujo integrado de comandos"""
        user_id = 'testuser'
        database.inicializar_album_completo(user_id)
        
        # Simular una serie de acciones
        database.update_cromo(user_id, 'ESP 1', 1)
        database.update_cromo(user_id, 'ESP 2', 1)
        
        # Verificar estado
        total, faltantes, repetidos = database.get_stats(user_id)
        assert faltantes == 657
        
        # Quitar uno
        database.update_cromo(user_id, 'ESP 1', -1)
        
        total, faltantes, repetidos = database.get_stats(user_id)
        assert faltantes == 658
