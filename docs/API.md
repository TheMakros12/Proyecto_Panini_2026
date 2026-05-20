# Documentación de la API

La aplicación web de Panini 2026 cuenta con varios endpoints para interactuar con la base de datos de manera programática. Todas las respuestas están en formato JSON.

### GET `/api/stats`
Obtiene las estadísticas de la colección del usuario.
- **Query Params**: `user_id` (Opcional, por defecto toma el configurado).
- **Respuesta**:
  ```json
  {
      "total": 638,
      "faltantes": 500,
      "conseguidos": 138,
      "repetidos": 10,
      "porcentaje": 21.6
  }
  ```

### GET `/api/faltantes`
Obtiene los cromos que faltan, agrupados por equipo.
- **Query Params**: `user_id`
- **Respuesta**:
  ```json
  {
      "ARG": [1, 2, 5],
      "ESP": [3, 4]
  }
  ```

### GET `/api/repetidos`
Obtiene los cromos repetidos, agrupados por equipo con sus respectivas cantidades.
- **Query Params**: `user_id`

### GET `/api/album`
Obtiene toda la estructura del álbum con las cantidades de cada cromo organizado por secciones y equipos.
- **Query Params**: `user_id`

### POST `/api/tengo`
Registra nuevos cromos en el álbum.
- **Body JSON**:
  ```json
  {
      "ids": "ARG 1, ESP 2",
      "user_id": "MarcosDB12"
  }
  ```

### POST `/api/quitar`
Resta cromos del álbum en caso de equivocación.
- **Body JSON**:
  ```json
  {
      "ids": "ARG 1",
      "user_id": "MarcosDB12"
  }
  ```

### GET `/api/historial`
Devuelve las últimas acciones registradas (cromos añadidos o eliminados).

### GET `/api/usuarios`
Obtiene una lista de todos los `user_id` registrados que tienen alguna interacción en la base de datos.

### POST `/api/update_name`
Actualiza el nombre de un jugador/cromo específico.
- **Body JSON**:
  ```json
  {
      "id": "ARG 10",
      "nombre": "Lionel Messi",
      "user_id": "MarcosDB12"
  }
  ```
