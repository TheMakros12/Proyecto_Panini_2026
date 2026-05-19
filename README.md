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

## 🚀 Instalación y Configuración

Sigue estos pasos para levantar tu propio servidor y bot en cuestión de minutos.

### 1. Clonar el repositorio
```bash
git clone https://github.com/TheMakros12/Proyecto_Panini_2026.git
cd Proyecto_Panini_2026
