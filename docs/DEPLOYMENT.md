# Guía de Despliegue (Deployment)

Este documento detalla cómo llevar la aplicación Panini 2026 Tracker a un entorno de producción (servidor en la nube, VPS, Railway, Render, etc.).

## 1. Configuración para Producción
En un entorno de producción, la base de datos de SQLite persistirá en el disco. Es importante asegurarse de que el servidor mantenga persistencia en la carpeta `instance/`.

### Variables de Entorno (`.env`)
Configura tus variables asegurándote de cambiar `WEB_URL` al dominio de tu servidor de producción:
```env
TELEGRAM_TOKEN=tu_token_de_telegram_real
WEB_URL=https://tudominio.com
DATABASE_PATH=instance/coleccion.db
FLASK_ENV=production
```

## 2. Ejecutar con Gunicorn (Linux/Mac)
Flask no debe ser ejecutado en producción usando su servidor de desarrollo integrado. Utiliza un servidor WSGI de producción como `gunicorn`.

1. Instala gunicorn:
```bash
pip install gunicorn
```

2. Ejecuta la aplicación web:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "src.app:app"
```

## 3. Ejecutar el Bot en Background
El bot de Telegram y la app web son dos procesos distintos. Puedes correr el bot utilizando un administrador de procesos como `supervisor`, `systemd`, o `pm2`.

Con `pm2` (requiere Node.js):
```bash
# Iniciar la web
pm2 start "gunicorn -w 4 -b 0.0.0.0:5000 src.app:app" --name "panini-web"

# Iniciar el bot
pm2 start "python main.py --mode bot --env production" --name "panini-bot"

# Guardar estado
pm2 save
```

## 4. Despliegue en Railway / Render
Si utilizas plataformas PaaS como Railway o Render:
- Define el **Start Command** para la web: `gunicorn src.app:app`
- Crea un servicio tipo "Worker" para el bot con el comando: `python main.py --mode bot`
- Configura las Environment Variables desde el panel de la plataforma.
- ¡Asegúrate de agregar un **Volume** persistente a la ruta `/instance` para que no se borre tu base de datos con cada despliegue!
