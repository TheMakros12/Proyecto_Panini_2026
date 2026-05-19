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
```

### 2. Instalar dependencias
Asegúrate de tener Python instalado y ejecuta:
```bash
pip install -r requirements.txt
```

### 3. Configurar el Bot de Telegram
Crea un bot en Telegram usando [BotFather](https://t.me/botfather) y obtén tu **Token**. Luego, configúralo como variable de entorno:

**En Windows (PowerShell):**
```powershell
$env:TELEGRAM_TOKEN="tu_token_aqui"
```

**En Linux / Mac:**
```bash
export TELEGRAM_TOKEN="tu_token_aqui"
```

### 4. Iniciar los servicios
Necesitarás dos terminales para correr el dashboard web y el bot simultáneamente.

* **Terminal 1 (Dashboard Web):**
  ```bash
  python app.py
  ```
  *La web estará disponible en `http://localhost:5000` o en la IP de tu PC en la red local.*

* **Terminal 2 (Bot de Telegram):**
  ```bash
  python bot.py
  ```

---

## 🎮 ¿Cómo se usa?

### 🌐 Vía Web
Accede a la IP de tu servidor desde el navegador. Verás tu progreso general y un desglose por grupos (A, B, C... FWC, CC, etc.). Haz clic sobre el número de los cromos para marcarlos como "conseguidos" o "repetidos" visualmente.

### 🤖 Vía Bot de Telegram
Inicia un chat con tu bot y utiliza los siguientes comandos:
* `/start` - Inicializa tu colección y muestra el menú de botones.
* `/tengo [ID]` - Registra cromos que acabas de conseguir (Ej: `/tengo ESP 1, ARG 5`).
* `/quitar [ID]` - Elimina cromos añadidos por error (Ej: `/quitar ESP 1`).
* `/falta` - Obtén una lista compacta de los cromos que necesitas para completar tu álbum.
* `/repetidos` - Mira rápidamente qué cromos tienes disponibles para intercambiar.
* `/estadisticas` - Visualiza un resumen instantáneo de tu progreso y % completado.

---

## 📂 Estructura del Proyecto

```text
Proyecto_Panini_2026/
├── app.py              # Servidor principal Web (Flask) y API REST
├── bot.py              # Lógica asíncrona y comandos del Bot de Telegram
├── database.py         # Inicialización del álbum completo y gestor SQLite
├── coleccion.db        # Base de datos (se genera automáticamente)
├── requirements.txt    # Dependencias del proyecto
├── static/             # Archivos CSS, JS e imágenes del frontend
└── templates/          # Plantillas HTML principales (index.html)
```

---

## 🤝 Contribuir
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la UI, añadir soporte para exportar las listas de repetidos a WhatsApp, u optimizar las queries, no dudes en hacer un *fork* del repositorio y enviar tu *Pull Request*.
