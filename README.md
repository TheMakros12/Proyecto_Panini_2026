# 🏆 Panini World Cup 2026 Tracker 🌍

¡Lleva el control total de tu colección de cromos del Mundial 2026 con estilo y facilidad! 

**Panini World Cup 2026 Tracker** es una plataforma dual (Aplicación Web + Bot de Telegram) diseñada para hacer que coleccionar e intercambiar cromos sea más divertido, rápido y organizado.

---

## ✨ Características Principales

* 💻 **Dashboard Web Moderno:** Interfaz con diseño *Glassmorphism* súper atractivo para visualizar y gestionar tu álbum de forma intuitiva.
* 🤖 **Bot de Telegram Integrado:** Añade o quita cromos directamente desde tu móvil usando comandos rápidos (`/tengo`, `/quitar`) o a través del menú de botones interactivos.
* 📊 **Estadísticas en Tiempo Real:** Mantén siempre a la vista tu progreso, porcentaje completado, y la cantidad exacta de faltantes y repetidos.
* 👥 **Soporte Multiusuario:** Cada usuario interactúa de forma independiente; todos pueden tener su propia colección guardada en la misma base de datos.
* 📱 **PWA Instalable:** Usa la aplicación web como una app nativa en tu dispositivo móvil (Android/iOS) para llevarla a donde vayas.

---

## 🛠️ Tecnologías y Arquitectura

Este proyecto está construido combinando un backend sólido con un frontend dinámico:

* **Backend:** [Python 3.8+](https://www.python.org/) + [Flask 3.0](https://flask.palletsprojects.com/) para servir la API REST y la web.
* **Base de Datos:** SQLite (`database.py`), ligera, rápida y sin necesidad de configuración adicional.
* **Integración:** `python-telegram-bot` v21.1 para la comunicación asíncrona con la API de Telegram.
* **Frontend:** HTML5, CSS3 (*Glass UI*), y JavaScript nativo para la carga dinámica a través de *endpoints* JSON.

---

## 🚀 Instalación Rápida

*(Para instrucciones detalladas de despliegue, revisa la carpeta `docs/`)*

### 1. Clonar e Instalar
```bash
git clone https://github.com/TheMakros12/Proyecto_Panini_2026.git
cd Proyecto_Panini_2026
pip install -r requirements.txt
```

### 2. Configurar el Entorno
Copia la plantilla de variables de entorno:
```bash
cp .env.example .env
```
Edita `.env` para añadir tu `TELEGRAM_TOKEN` (obtenido desde BotFather).

### 3. Iniciar la Aplicación
El proyecto tiene un único punto de entrada unificado (`main.py`):
```bash
# Ejecutar ambos (Web + Bot):
python main.py --mode both

# Ejecutar solo Web:
python main.py --mode web

# Ejecutar solo Bot:
python main.py --mode bot
```
*La web estará disponible en `http://localhost:5000` o en la IP de tu PC en la red local.*

---

## 📚 Documentación Completa

Toda la documentación técnica se ha movido a la carpeta `docs/` para mantener el repositorio limpio:
- 📖 [**Guía de Instalación Detallada**](docs/INSTALL.md)
- ⚙️ [**API Endpoints**](docs/API.md)
- 🤖 [**Comandos del Bot de Telegram**](docs/BOT_COMMANDS.md)
- 🚀 [**Guía de Despliegue (Producción)**](docs/DEPLOYMENT.md)

---

## 📂 Estructura del Proyecto

```text
Proyecto_Panini_2026/
├── src/                # Código fuente principal
│   ├── app.py          # Aplicación Web Flask y API
│   ├── bot.py          # Bot de Telegram
│   └── database.py     # Gestor de base de datos SQLite
├── docs/               # Documentación técnica
├── static/             # Recursos públicos (CSS, JS, imágenes)
├── templates/          # Plantillas HTML
├── tests/              # Pruebas unitarias
├── instance/           # Base de datos local (creada automáticamente)
├── config.py           # Configuraciones centralizadas
├── main.py             # Punto de entrada unificado
├── .env.example        # Plantilla de variables de entorno
└── requirements.txt    # Dependencias
```

---

## 🤝 Contribuir
¡Las contribuciones son bienvenidas! Todavía sigo en fase de implementar algunas cosas nuevas pero, si tienes ideas para mejorar la UI, añadir soporte para exportar las listas de repetidos a WhatsApp, u optimizar las queries, no dudes en hacer un *fork* del repositorio y enviar tu *Pull Request*.
