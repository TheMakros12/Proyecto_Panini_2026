# Comandos del Bot de Telegram

Interactúa con tu colección directamente desde Telegram utilizando los siguientes comandos:

## Comandos Principales

### `/start`
Inicia la colección (o la retoma si ya existe) y muestra el menú interactivo principal con botones para ver tus estadísticas, faltantes, repetidos o abrir la aplicación web.

### `/tengo <CROMOS>`
Registra uno o varios cromos que acabas de conseguir en el álbum.
- **Ejemplo**: `/tengo ARG 1, ESP 5, FWC 10`
- **Nota**: Puedes usar minúsculas o mayúsculas, el bot lo interpretará correctamente. Separa los cromos con comas.

### `/quitar <CROMOS>`
Elimina cromos de tu colección en caso de haberlos registrado por error o haberlos intercambiado.
- **Ejemplo**: `/quitar ARG 1, MEX 4`

### `/falta`
Te envía una lista detallada de todos los cromos que aún te faltan para completar el álbum, agrupados por equipo y formateados en rangos (ej: `1-5, 8, 10-15`).

### `/repetidos`
Te muestra la lista de cromos que tienes repetidos, indicando cuántos extras tienes de cada uno.

### `/estadisticas`
Muestra un resumen rápido de tu progreso:
- Total de cromos conseguidos y porcentaje completado.
- Cantidad de cromos faltantes.
- Cantidad de cromos repetidos en total.

### `/web`
Genera el enlace para abrir tu Dashboard Visual en el navegador.

## Interacción con Botones
Además de comandos de texto, el comando `/start` habilita una botonera interactiva para realizar consultas rápidas sin tener que escribir los comandos de nuevo.
