# Software Engineer Challenge

## Overview

Welcome to the Software Engineer Application Challenge. In this challenge, you will demonstrate your skills in backend development, API design, testing, and cloud deployment.

## Problem

You will develop a RESTful API for user management with complete CRUD (Create, Read, Update, Delete) operations. The application should handle user data with the following attributes:

| Field      | Description                              |
| ---------- | ---------------------------------------- |
| id         | Unique identifier for each user          |
| username   | User's unique username                   |
| email      | User's email address                     |
| first_name | User's first name                        |
| last_name  | User's last name                         |
| role       | User role (admin, user, guest)           |
| created_at | Timestamp when the user was created      |
| updated_at | Timestamp when the user was last updated |
| active     | Boolean indicating if the user is active |

## Challenge

### Context:

In today's digital landscape, effective user management is a foundational component of virtually all software applications. This challenge simulates a real-world scenario where a user management API is needed for a growing application.

As a Software Engineer, you've been tasked with building a robust and scalable user management API that will serve as the backbone for user-related operations. The API should provide a clean interface for creating, retrieving, updating, and deleting user profiles while ensuring data integrity and following industry best practices.

Beyond just functionality, we're interested in seeing your approach to software architecture, code organization, testing strategies, and cloud deployment skills. This challenge is designed to showcase not only your technical abilities but also your understanding of production-ready software development.

### API Development

Develop an API with FastAPI:

- Implement all CRUD endpoints for user management
- Add proper input validation for all requests
- Document all endpoints using OpenAPI/Swagger
- Implement proper error handling for edge cases
- The API should connect to a database of your choice (SQL or NoSQL)
- Write detailed API tests using pytest
- Deploy your API to Google Cloud Platform (GCP)

Requirements:

- You must use FastAPI as the framework
- Provide examples of API calls for each endpoint in your documentation
- Write clean, maintainable code with proper comments
- The API should follow REST best practices
- Include at least basic logging functionality
- Create a `cloudbuild.yaml` file for Google Cloud Build that includes:
  - Building the Docker image
  - Running tests
  - Deploying the application to Google Cloud Run or App Engine

### Evaluation Criteria

Your submission will be evaluated based on the following criteria:

- **Code Quality**: Readability, organization, and adherence to Python best practices
- **API Design**: Proper implementation of RESTful principles and resource modeling
- **Data Handling**: Effective data validation, error handling, and database integration
- **Testing**: Comprehensive test coverage and proper test organization
- **Documentation**: Clear and complete API documentation
- **Cloud Deployment**: Successful deployment to GCP and proper configuration
- **CI/CD Implementation**: Quality and completeness of the `cloudbuild.yaml` file
- **Overall Functionality**: The API works as expected for all CRUD operations

### Submission Instructions

To submit your challenge, you must do a POST request to: https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/software-engineer

This is an example of the body you must send:

```json
{
  "name": "Juan Perez",
  "mail": "juan.perez@example.com",
  "github_url": "https://github.com/juanperez/se-challenge.git",
  "api_url": "https://juan-perez.api"
}
```

PLEASE, SEND THE REQUEST ONLY ONCE.
If your request was successful, you will receive this message:

```
jsonCopiar{
  "status": "OK",
  "detail": "your request was received"
}
```

NOTE: We recommend sending the challenge even if you didn't manage to finish all the parts.

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
