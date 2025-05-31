# Software Engineer Challenge

## Configuración del Entorno de Desarrollo

1.  **Clonar el repositorio**:

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd user-management-api
    ```

2.  **Crear un entorno virtual** (recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # venv\Scripts\activate  # En Windows
    ```

3.  **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

## Gestión de Migraciones con Alembic

Después de configurar el entorno, debes inicializar Alembic y generar tu primera migración.

1.  **Inicializar Alembic**:
    Si aún no lo has hecho, ejecuta este comando desde la raíz del proyecto:

    ```bash
    alembic init migrations
    ```

    Esto creará el directorio `migrations/` y el archivo `alembic.ini`.

2.  **Generar la primera migración**:
    Alembic detectará los modelos definidos en `app/models.py` y generará un script para crear la tabla `users`.

    ```bash
    alembic revision --autogenerate -m "Create initial user table"
    ```

    Revisa el archivo generado en `migrations/versions/` para asegurarte de que las operaciones son correctas.

3.  **Aplicar las migraciones (localmente)**:
    Esto creará la tabla `users` y la tabla `alembic_version` en tu base de datos local (`sql_app.db`).
    ```bash
    alembic upgrade head
    ```

### Flujo de Trabajo de Migraciones

- **Cuando modificas tus modelos (`app/models.py`)**:
  1.  Realiza los cambios en tus modelos.
  2.  Genera un nuevo script de migración: `alembic revision --autogenerate -m "Descripción de tu cambio"`
  3.  Revisa el script generado.
  4.  Aplica la migración localmente: `alembic upgrade head`

## Ejecución Local

1.  **Asegúrate de que las migraciones estén aplicadas** (ver sección anterior).

2.  **Iniciar la aplicación**:

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

    La opción `--reload` permite que el servidor se recargue automáticamente al detectar cambios en el código.

3.  **Acceder a la API**:
    - La API estará disponible en `http://127.0.0.1:8000`.
    - La documentación interactiva (Swagger UI) estará en `http://127.0.0.1:8000/docs`.
    - La documentación alternativa (ReDoc) estará en `http://127.0.0.1:8000/redoc`.

## Ejemplos de Llamadas a la API

Puedes usar `curl`, Postman, Insomnia o la propia interfaz de Swagger UI para probar los endpoints.

### 1. Crear un nuevo usuario (`POST /users/`)

**Request Body:**

```json
{
  "username": "jane_doe",
  "email": "jane.doe@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "role": "user",
  "active": true
}
```
