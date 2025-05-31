import os

from pydantic import AnyHttpUrl
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  PROJECT_NAME: str = "LATAM-API"

  SQLALCHEMY_DATABASE_URL: ClassVar[str] =  os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./sql_app.db")


settings = Settings()
