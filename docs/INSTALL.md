# Instalación

Sigue estos pasos para configurar e instalar el proyecto en tu máquina local.

## 1. Requisitos Previos
- Python 3.9 o superior
- Pip (Gestor de paquetes de Python)
- Git

## 2. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Proyecto_Panini_2026
```

## 3. Crear entorno virtual (Recomendado)
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

## 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 5. Configurar Variables de Entorno
Copia el archivo `.env.example` a un nuevo archivo llamado `.env` en la raíz del proyecto y agrega tu token de Telegram:
```bash
cp .env.example .env
```
Abre `.env` y asegúrate de configurar correctamente:
- `TELEGRAM_TOKEN`: El token de tu bot obtenido desde BotFather en Telegram.
- `WEB_URL`: URL donde corre tu aplicación web (ej: http://localhost:5000).

## 6. Ejecutar la aplicación
El proyecto tiene un punto de entrada único `main.py`. Puedes ejecutar la app web, el bot, o ambos:
```bash
# Para ejecutar ambos (la web en primer plano y te recomendará abrir otra terminal para el bot)
python main.py --mode both

# Para ejecutar solo la app web
python main.py --mode web

# Para ejecutar solo el bot
python main.py --mode bot
```

Una vez iniciada la web, abre tu navegador en `http://localhost:5000`.
