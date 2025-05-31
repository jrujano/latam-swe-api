import os
from logging.config import fileConfig

from dotenv import load_dotenv  # Carga las variables de entorno
from sqlalchemy import engine_from_config, pool

from alembic import context
from app.db.base import Base

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

config = context.config
fileConfig(config.config_file_name)


target_metadata = Base.metadata


def get_url():

    SQLALCHEMY_DATABASE_URL: str = os.getenv(
        "SQLALCHEMY_DATABASE_URL", "sqlite:///./sql_app.db"
    )

    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
            "postgres://", "postgresql://", 1
        )

    print(
        f"Connecting to database: {SQLALCHEMY_DATABASE_URL}"
    )  # Imprime la URL para depuración
    return SQLALCHEMY_DATABASE_URL


def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
