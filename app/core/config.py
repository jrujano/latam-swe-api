import os
from typing import ClassVar

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  PROJECT_NAME: str = "LATAM-API"

  SQLALCHEMY_DATABASE_URL: ClassVar[str] =  os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./sql_app.db")
  SECRET_KEY: str = os.getenv("SECRET_KEY", "LATAM")
  # Algoritmo de encriptación (ALGORITHM)

  # Tiempo de expiración del token (ACCESS_TOKEN_EXPIRE_MINUTES)
  ACCESS_TOKEN_EXPIRE_MINUTES: str = Field(default='30')
  REFRESH_TOKEN_EXPIRE_MINUTES: str = Field(default='10800') # 7 días para refresh token
  ALGORITHM: str = Field(
        default='HS256',
        description="Algoritmo para JWT",
        pattern=r'^(HS256|HS384|HS512|RS256|RS384|RS512|ES256|ES384|ES512)$'
    )
  


settings = Settings()
