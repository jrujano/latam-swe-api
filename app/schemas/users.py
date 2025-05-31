from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Esquema base para los atributos comunes del usuario.
    """

    username: str = Field(..., min_length=3, max_length=50, example="jrujano")
    email: EmailStr = Field(..., example="jrujano@gmail.com")
    first_name: Optional[str] = Field(None, max_length=50, example="Johan")
    last_name: Optional[str] = Field(None, max_length=50, example="Rujano")
    role: str = Field("user", pattern="^(admin|user|guest)$", example="user")
    active: Optional[bool] = Field(True, example=True)


class UserCreate(UserBase):
    """
    Esquema para la creación de un nuevo usuario.
    """

    # No se añaden campos adicionales aquí, ya que UserBase contiene lo necesario para la creación.
    pass


class UserUpdate(BaseModel):
    """
    Esquema para la actualización de un usuario existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """

    username: Optional[str] = Field(
        None, min_length=3, max_length=50, example="jrujano_updated"
    )
    email: Optional[EmailStr] = Field(None, example="jrujano@gmail.com")
    first_name: Optional[str] = Field(None, max_length=50, example="Johan J")
    last_name: Optional[str] = Field(None, max_length=50, example="Rujano")
    role: Optional[str] = Field(None, pattern="^(admin|user|guest)$", example="admin")
    active: Optional[bool] = Field(None, example=False)


class UserResponse(UserBase):
    """
    Esquema para la respuesta de un usuario.
    Incluye campos generados por la base de datos como 'id', 'created_at', 'updated_at'.
    """

    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2023-10-26T10:00:00.000000")
    updated_at: datetime = Field(..., example="2023-10-26T10:00:00.000000")

    class Config:
        """
        Configuración para habilitar el modo ORM.
        Esto permite que Pydantic lea datos directamente de modelos de SQLAlchemy.
        """

        from_attributes = True  # Anteriormente orm_mode = True en Pydantic v1
