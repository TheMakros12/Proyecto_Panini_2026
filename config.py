import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base"""
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    WEB_URL = os.getenv('WEB_URL', 'http://localhost:5000')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'instance/coleccion.db')
    DEFAULT_USER = 'MarcosDB12'
    DEBUG = False
    FLASK_ENV = 'development'
    TEMPLATES_FOLDER = 'templates'
    STATIC_FOLDER = 'static'

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    FLASK_ENV = 'production'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
