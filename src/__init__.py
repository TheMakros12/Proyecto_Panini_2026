"""
Proyecto Panini 2026 - Módulo principal
Contiene la aplicación Flask y el bot de Telegram
"""

from src.app import app
from src.bot import get_bot_application

__version__ = '1.0.0'
__author__ = 'TheMakros12'
__all__ = ['app', 'get_bot_application']
