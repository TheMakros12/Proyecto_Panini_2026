#!/usr/bin/env python
"""Punto de entrada único para Panini World Cup 2026 Tracker

Uso:
    python main.py --mode web         # Solo la aplicación web
    python main.py --mode bot         # Solo el bot de Telegram
    python main.py --mode both        # Ambos (requiere 2 terminales)
    python main.py --env production   # Usar configuración de producción
"""

import sys
import argparse
import logging
from src import database
from config import config, Config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description='🏆 Panini World Cup 2026 Tracker',
        epilog='Ejemplo: python main.py --mode web --env development'
    )
    
    parser.add_argument(
        '--mode',
        choices=['web', 'bot', 'both'],
        default='both',
        help='Qué componente ejecutar (default: both)'
    )
    
    parser.add_argument(
        '--env',
        choices=['development', 'production'],
        default='development',
        help='Entorno a usar (default: development)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Puerto para la aplicación web (default: 5000)'
    )
    
    args = parser.parse_args()
    
    # Configurar entorno
    cfg = config[args.env]
    logger.info(f"🔧 Configurando entorno: {args.env}")
    logger.info(f"📂 Base de datos: {cfg.DATABASE_PATH}")
    logger.info(f"🌐 URL Web: {cfg.WEB_URL}")
    
    # Inicializar base de datos
    logger.info("📦 Inicializando base de datos...")
    database.init_db()
    
    try:
        if args.mode in ['web', 'both']:
            logger.info(f"🚀 Iniciando aplicación web en puerto {args.port}...")
            from src.app import app
            
            if args.mode == 'web':
                # Solo web
                app.run(
                    debug=cfg.DEBUG,
                    host='0.0.0.0',
                    port=args.port,
                    use_reloader=False
                )
            else:
                # Both - web en background
                logger.warning("⚠️  Ejecutando ambos. La web se ejecutará en el foreground.")
                logger.warning("💡 Abre otra terminal y ejecuta: python main.py --mode bot")
                app.run(
                    debug=cfg.DEBUG,
                    host='0.0.0.0',
                    port=args.port,
                    use_reloader=False
                )
        
        if args.mode in ['bot', 'both']:
            logger.info("🚀 Iniciando bot de Telegram...")
            from src.bot import main as bot_main
            bot_main()
    
    except KeyboardInterrupt:
        logger.info("⏹️  Deteniendo aplicación...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
