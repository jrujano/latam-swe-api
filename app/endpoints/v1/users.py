# Endpoints CRUD para usuarios
import logging
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core import deps

router = APIRouter()

logging.basicConfig(
    format="%(asctime)s %(levelname)-5s [%(filename)s:%(lineno)d]\n%(message)s\n",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@router.post(
    "/users/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    response_description="El usuario recién creado",
    description="Crea un nuevo perfil de usuario con un nombre de usuario y correo electrónico únicos.",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Nombre de usuario o correo electrónico ya existe"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Error de validación de entrada"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno del servidor"
        },
    },
)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    """
    Crea un nuevo usuario en la base de datos.
    - **username**: Nombre de usuario único.
    - **email**: Dirección de correo electrónico única.
    - **first_name**: Nombre del usuario (opcional).
    - **last_name**: Apellido del usuario (opcional).
    - **role**: Rol del usuario (admin, user, guest). Por defecto "user".
    - **active**: Booleano que indica si el usuario está activo. Por defecto True.
    """
    try:
        # Validar si el username ya existe
        existing_username = crud.crud_user.get_user_by_username(db, user.username)
        existing_email = crud.crud_user.get_user_by_email(db, user.email)

        if existing_username or existing_email:
            if existing_email:
                detail_error = "La dirección de correo electrónico ya existe."
                logger.warning(detail_error)
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=detail_error,
                )
            else:
                detail_error = "El nombre de usuario ya existe."
                logger.warning(detail_error)
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=detail_error,
                )

        db_user = crud.crud_user.create(db=db, obj_in=user)
        return db_user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al crear usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get(
    "/users/",
    response_model=List[schemas.UserResponse],
    summary="Obtener todos los usuarios",
    response_description="Lista de usuarios",
    description="Recupera una lista de todos los perfiles de usuario, con opciones de paginación.",
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Recupera una lista de usuarios.
    - **skip**: Número de usuarios a omitir (para paginación).
    - **limit**: Número máximo de usuarios a devolver.
    """
    try:
        logger.info(f"Recuperando usuarios (skip: {skip}, limit: {limit}).")
        users = crud.crud_user.get_multi(db, skip=skip, limit=limit)
        logger.info(f"Se recuperaron {len(users)} usuarios.")
        return users
    except Exception as e:
        logger.error(f"Error inesperado al recuperar usuarios: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
    summary="Obtener un usuario por ID",
    response_description="El usuario solicitado",
    description="Recupera un perfil de usuario específico por su ID único.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Usuario no encontrado"}},
)
def read_user(user_id: int, db: Session = Depends(deps.get_db)):
    """
    Recupera un usuario por su ID.
    - **user_id**: El ID del usuario a recuperar.
    """
    try:
        db_user = crud.crud_user.get(db, id=user_id)
        if db_user is None:
            logger.warning(f"Usuario con ID {user_id} no encontrado.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return db_user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al recuperar usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
    summary="Actualizar un usuario existente",
    response_description="El usuario actualizado",
    description="Actualiza un perfil de usuario existente por su ID. Los campos no proporcionados no se modifican.",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Usuario no encontrado"},
        status.HTTP_409_CONFLICT: {
            "description": "Nombre de usuario o correo electrónico ya existe"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Error de validación de entrada"
        },
    },
)
def update_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(deps.get_db)
):
    """
    Actualiza un usuario existente.
    - **user_id**: El ID del usuario a actualizar.
    - **user**: Objeto con los campos a actualizar (opcionales).
    """
    try:

        # Obtener usuario actual
        db_user_actual = crud.crud_user.get(db, id=user_id)
        if db_user_actual is None:
            logger.warning(
                f"No se pudo actualizar: Usuario con ID {user_id} no encontrado."
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        # Validar username si fue modificado
        if user.username and user.username != db_user_actual.username:
            existing_username = crud.crud_user.get_user_by_username(db, user.username)
            if existing_username and existing_username.id != user_id:
                logger.warning(f"El nombre de usuario '{user.username}' ya existe.")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El nombre de usuario ya existe.",
                )

        # Validar email si fue modificado
        if user.email and user.email != db_user_actual.email:
            existing_email = crud.crud_user.get_user_by_email(db, user.email)
            if existing_email and existing_email.id != user_id:
                logger.warning(
                    f"La dirección de correo electrónico '{user.email}' ya existe."
                )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="La dirección de correo electrónico ya existe.",
                )

        db_user = crud.crud_user.update(db, db_obj=db_user_actual, obj_in=user)
        return db_user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al actualizar usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
    response_description="No Content",
    description="Elimina un perfil de usuario por su ID único.",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Usuario no encontrado"}},
)
def delete_user(user_id: int, db: Session = Depends(deps.get_db)):
    """
    Elimina un usuario por su ID.
    - **user_id**: El ID del usuario a eliminar.
    """
    try:
        db_user_actual = crud.crud_user.get(db, id=user_id)
        if db_user_actual:
            success = crud.crud_user.remove(db=db, id=user_id)
            if not success:
                logger.warning(f"No se pudo eliminar: Usuario con ID {user_id} no encontrado.")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
                )
            return {
                "message": "Usuario eliminado con éxito"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al eliminar usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )