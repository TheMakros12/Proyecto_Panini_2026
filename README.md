# Panini World Cup 2026 Tracker

Una aplicación web completa y bot de Telegram para llevar el seguimiento de tu colección de cromos del Mundial Panini 2026.

## Funcionalidades
* **Dashboard Web:** Interfaz gráfica moderna (Glassmorphism) para añadir o borrar cromos visualmente.
* **Soporte Multiusuario:** Varias personas pueden llevar sus colecciones de forma independiente.
* **Estadísticas en Tiempo Real:** Porcentaje completado, cromos faltantes y repetidos.
* **Integración con Telegram:** Bot interactivo que permite añadir, borrar y consultar la colección desde el chat mediante botones o comandos.
* **Exportación a WhatsApp:** Formato automático de las listas de faltantes y repetidos para facilitar los intercambios.
* **PWA Instalable:** Puede instalarse como aplicación nativa en dispositivos móviles (Android/iOS).

## Requisitos
* Python 3.8+
* `pip install -r requirements.txt` (Flask, python-telegram-bot, httpx)

## Uso
1. Configurar la variable de entorno para el bot de Telegram:
   ```bash
   export TELEGRAM_TOKEN="tu-token-aqui"
   ```
   *(En Windows PowerShell: `$env:TELEGRAM_TOKEN="tu-token-aqui"`)*

2. Iniciar el servidor Web (Backend y DB):
   ```bash
   python app.py
   ```
   *Acceso desde el navegador web en `http://localhost:5000` o la IP local de tu ordenador.*

3. En otra terminal, iniciar el Bot de Telegram:
   ```bash
   python bot.py
   ```
