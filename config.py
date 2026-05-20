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
    TESTING = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Configuración para testing"""
    DEBUG = True
    TESTING = True
    DATABASE_PATH = 'instance/test_coleccion.db'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(env='default'):
    """Obtener configuración según el entorno"""
    return config.get(env, config['default'])
