#!/bin/bash
echo "Corriendo migraciones"
alembic upgrade head
echo "Ajuste de BD realizados....."


echo "Iniciando servidor" 
exec uvicorn app.main:app --host=0.0.0.0 --port=8080