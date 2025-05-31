# -*- coding: utf-8 -*-
from typing import Optional

from app.schemas.users import UserBase
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.users import User


class CRUDUser(CRUDBase[User, UserBase, UserBase]):
    def get_user_by_username(self, db: Session, username: str):
        """
        Obtiene un usuario por su nombre de usuario.
        """
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str):
        """
        Obtiene un usuario por su nombre de usuario.
        """
        return db.query(User).filter(User.email == email).first()


crud_user = CRUDUser(User)
