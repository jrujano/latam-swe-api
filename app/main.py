# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from .endpoints.routes import api_router_v1

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="API de Gestión de Usuarios",
    description="Una API RESTful completa para gestionar usuarios con operaciones CRUD.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.include_router(api_router_v1)
# Evento de inicio: las tablas serán gestionadas por Alembic.
@app.on_event("startup")
def on_startup():
    """
    Se ejecuta al iniciar la aplicación.
    Las tablas serán gestionadas por Alembic, así que no se usa create_all aquí.
    """
    logger.info("Iniciando la aplicación.")
    # Base.metadata.create_all(bind=engine) # <-- LÍNEA ELIMINADA: Alembic gestiona las migraciones
    logger.info("Tablas de la base de datos gestionadas por Alembic.")

# Endpoint de prueba para verificar que la API está funcionando
@app.get("/", summary="Verificar estado de la API", response_description="Mensaje de bienvenida")
def read_root():
    """
    Endpoint simple para verificar que la API está en funcionamiento.
    """
    logger.info("Solicitud recibida en el endpoint raíz.")
    return {"message": "Bienvenido a la API de Gestión de Usuarios"}

