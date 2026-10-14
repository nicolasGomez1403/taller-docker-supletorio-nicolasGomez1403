## Arranque local

```bash
uv sync
uv run uvicorn reservas.api:app --port 8500
```

`uv sync` crea el entorno `.venv` e instala las versiones exactas que fija `uv.lock`, incluidas las de desarrollo.

- Estado: `http://127.0.0.1:8500/estado`
- Motor de base de datos en uso: `http://127.0.0.1:8500/motor`
- Registro y listado: `POST` y `GET` en `http://127.0.0.1:8500/reservas`, con cuerpo `{"sala": "...", "responsable": "...", "franja": "..."}`

## Pruebas

```bash
uv run pytest
```

## Base de datos

Por defecto persiste en `instancia/reservas.db` (SQLite) y crea la carpeta `instancia/` al arrancar. Para usar MariaDB, define antes de arrancar `RESERVAS_DB_HOST`, `RESERVAS_DB_USUARIO`, `RESERVAS_DB_CLAVE` y `RESERVAS_DB_NOMBRE`, y `RESERVAS_DB_PUERTO` si no es 3306.
