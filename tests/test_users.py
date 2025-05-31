# tests/test_users.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.deps import get_db
from app.db.base import Base
from app.main import app
from app.models.users import User

# Configuración de la base de datos de prueba
# Usamos una base de datos SQLite en memoria para las pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"  # Usamos un archivo para que las pruebas puedan ver los cambios
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

API_VERSION_URL = "api/v1"
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Sobreescribe la dependencia get_db para usar la base de datos de prueba
@pytest.fixture(name="db_session")
def db_session_fixture():
    """
    Fixture para una sesión de base de datos de prueba.
    Crea las tablas antes de cada prueba y las elimina después.
    """
    Base.metadata.create_all(bind=engine)  # Crea las tablas
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Elimina las tablas después de la prueba


@pytest.fixture(name="client")
def client_fixture(db_session):
    """
    Fixture para el cliente de prueba de FastAPI.
    Usa la base de datos de prueba.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()  # Asegura que la sesión se cierre

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()  # Limpia las sobreescrituras después de la prueba


# --- Pruebas de Endpoints CRUD ---


def test_create_user(client):
    """
    Prueba la creación de un usuario con datos válidos.
    """
    print(f"{API_VERSION_URL}/users/")
    response = client.post(
        f"{API_VERSION_URL}/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
            "active": True,
        },
    )
    assert response.status_code == 201
    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_user_duplicate_username(client):
    """
    Prueba la creación de un usuario con un nombre de usuario duplicado.
    Debería devolver un error 409.
    """
    client.post(
        f"{API_VERSION_URL}/users/",
        json={"username": "duplicate", "email": "unique1@example.com"},
    )
    response = client.post(
        f"{API_VERSION_URL}/users/",
        json={"username": "duplicate", "email": "unique2@example.com"},
    )
    data = response.json()
    print(data)
    assert response.status_code == 409
    assert "El nombre de usuario ya existe." in response.json()["detail"]


def test_create_user_duplicate_email(client):
    """
    Prueba la creación de un usuario con un correo electrónico duplicado.
    Debería devolver un error 409.
    """
    client.post(
        f"{API_VERSION_URL}/users/",
        json={"username": "user1", "email": "duplicate@example.com"},
    )
    response = client.post(
        f"{API_VERSION_URL}/users/",
        json={"username": "user2", "email": "duplicate@example.com"},
    )
    assert response.status_code == 409
    assert "La dirección de correo electrónico ya existe." in response.json()["detail"]


def test_create_user_invalid_role(client):
    """
    Prueba la creación de un usuario con un rol inválido.
    Debería devolver un error 422.
    """
    response = client.post(
        f"{API_VERSION_URL}/users/",
        json={
            "username": "invalidrole",
            "email": "invalid@example.com",
            "role": "superadmin",
        },
    )
    assert response.status_code == 422
    assert "string_pattern_mismatch" in response.json()["detail"][0]["type"]


def test_get_users(client):
    """
    Prueba la recuperación de todos los usuarios.
    """
    client.post(
        f"{API_VERSION_URL}/users/",
        json={"username": "user1", "email": "user1@example.com"},
    )
    client.post(
        f"{API_VERSION_URL}/users/",
        json={"username": "user2", "email": "user2@example.com"},
    )
    response = client.get(f"{API_VERSION_URL}/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["username"] == "user1"
    assert data[1]["username"] == "user2"


def test_get_user_by_id(client):
    """
    Prueba la recuperación de un usuario por su ID.
    """
    create_response = client.post(
        f"{API_VERSION_URL}/users/",
        json={"username": "user_id_test", "email": "user_id@example.com"},
    )
    user_id = create_response.json()["id"]

    response = client.get(f"{API_VERSION_URL}/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "user_id_test"


def test_get_non_existent_user(client):
    """
    Prueba la recuperación de un usuario que no existe.
    Debería devolver un error 404.
    """
    response = client.get(f"{API_VERSION_URL}/users/999")
    assert response.status_code == 404
    assert "Usuario no encontrado" in response.json()["detail"]


def test_update_user(client):
    """
    Prueba la actualización de un usuario existente.
    """
    create_response = client.post(
        f"{API_VERSION_URL}/users/",
        json={"username": "update_me", "email": "update@example.com"},
    )
    user_id = create_response.json()["id"]

    response = client.put(
        f"{API_VERSION_URL}/users/{user_id}",
        json={
            "username": "updated_user",
            "email": "updated@example.com",
            "role": "admin",
            "active": 0
        },
    )
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["id"] == user_id
    assert data["username"] == "updated_user"
    assert data["email"] == "updated@example.com"
    assert data["role"] == "admin"
    assert data["active"] == False
 

def test_update_user_partial(client):
    """
    Prueba la actualización parcial de un usuario.
    """
    create_response = client.post(
       f"{API_VERSION_URL}/users",
        json={
            "username": "partial_update",
            "email": "partial@example.com",
            "first_name": "Original",
        },
    )
    user_id = create_response.json()["id"]

    response = client.put(f"{API_VERSION_URL}/users/{user_id}", json={"first_name": "New Name"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["first_name"] == "New Name"
    assert (
        data["username"] == "partial_update"
    )  # Asegura que otros campos no se modificaron


def test_update_non_existent_user(client):
    """
    Prueba la actualización de un usuario que no existe.
    Debería devolver un error 404.
    """
    response = client.put(
        f"{API_VERSION_URL}/users/999", json={"username": "non_existent", "email": "non@example.com"}
    )
    assert response.status_code == 404
    assert "Usuario no encontrado" in response.json()["detail"]


def test_update_user_duplicate_username(client):
    """
    Prueba la actualización de un usuario con un nombre de usuario ya existente.
    Debería devolver un error 409.
    """
    client.post(
        f"{API_VERSION_URL}/users/", json={"username": "existing_user", "email": "exist@example.com"}
    )
    create_response = client.post(
       f"{API_VERSION_URL}/users/", json={"username": "another_user", "email": "another@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.put(f"{API_VERSION_URL}/users/{user_id}", json={"username": "existing_user"})
    assert response.status_code == 409
    print("response.json()['detail']")
    assert (
        "El nombre de usuario ya existe."
        in response.json()["detail"]
    )



def test_delete_user(client):
    """
    Prueba la eliminación de un usuario existente.
    """
    create_response = client.post(
        f"{API_VERSION_URL}/users/", json={"username": "delete_me", "email": "delete@example.com"}
    )
    user_id = create_response.json()["id"]

    response = client.delete(f"{API_VERSION_URL}/users/{user_id}")
    assert response.status_code == 204  # No Content

    # Verificar que el usuario ha sido eliminado
    get_response = client.get(f"{API_VERSION_URL}/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_non_existent_user(client):
    """
    Prueba la eliminación de un usuario que no existe.
    Debería devolver un error 404.
    """
    response = client.delete(f"{API_VERSION_URL}/users/999")
    assert response.status_code == 404
    assert "Usuario no encontrado" in response.json()["detail"]
