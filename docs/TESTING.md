# Pruebas (Testing)

Este documento explica cómo ejecutar y verificar las pruebas automatizadas del proyecto Panini 2026 Tracker.

## 1. Requisitos Previos
- Python 3.9 o superior
- Un entorno virtual Python activo (`venv`, `virtualenv`, etc.)
- Dependencias instaladas desde `requirements.txt`

## 2. Instalar dependencias
Si no lo has hecho aún, instala los paquetes necesarios:
```bash
pip install -r requirements.txt
```

## 3. Ejecutar todas las pruebas
El proyecto utiliza `pytest` para las pruebas unitarias.

```bash
pytest
```

Esto ejecutará todas las pruebas que se encuentran en la carpeta `tests/`.

## 4. Ejecutar pruebas específicas
Puedes ejecutar un único archivo de prueba o un subconjunto de casos de prueba:

```bash
pytest tests/test_database.py
pytest tests/test_app.py
pytest tests/test_bot.py
```

También puedes ejecutar una sola prueba dentro de un archivo:

```bash
pytest tests/test_app.py -k "test_stats_empty_album"
```

## 5. Generar reporte de cobertura
El proyecto incluye `pytest-cov` para medir cobertura de código.

```bash
pytest --cov=src
```

Esto mostrará un resumen de cobertura en la consola.

## 6. Contenido de las pruebas
Las pruebas se agrupan en los siguientes archivos:

- `tests/test_database.py`
  - Verifica la conexión a SQLite y las operaciones de base de datos.
  - Comprueba normalización de IDs, inicialización del álbum, actualizaciones de cromos y estadísticas.

- `tests/test_app.py`
  - Prueba el servidor Flask y los endpoints JSON.
  - Valida las rutas `/api/stats`, `/api/faltantes`, `/api/repetidos`, `/api/album`, `/api/tengo`, entre otras.

- `tests/test_bot.py`
  - Comprueba la lógica interna del bot de Telegram.
  - Incluye pruebas de formateo de rangos, generación de estadísticas, faltantes y repetidos.

## 7. Uso de base de datos temporal
Las pruebas utilizan una base de datos SQLite temporal para no afectar los datos reales.

- Cada prueba crea un archivo `.db` temporal.
- Se actualiza la ruta de `database.DB_PATH` y `Config.DATABASE_PATH` durante la ejecución.
- Al finalizar, el archivo temporal se elimina automáticamente.

## 8. Buenas prácticas
- Ejecuta las pruebas después de hacer cambios en `src/` o en la lógica del bot.
- Usa pruebas específicas para acelerar el desarrollo cuando trabajes en una sola parte del proyecto.
- Si agregas nueva funcionalidad, agrega pruebas nuevas en el archivo correspondiente dentro de `tests/`.

## 9. Problemas comunes
- Si `pytest` no se encuentra, revisa que estés usando el entorno virtual correcto y que `pytest` esté instalado.
- Si las pruebas no pasan por dependencias faltantes, ejecuta nuevamente:
```bash
pip install -r requirements.txt
```

---

Con esto puedes validar la funcionalidad del proyecto y mantener la calidad de la aplicación web y del bot de Telegram.