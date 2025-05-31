# scripts/run_app.sh
#!/bin/bash

echo "Running database migrations..."
# SQLALCHEMY_DATABASE_URL se espera que esté configurada en el entorno de Cloud Run
# o como un secreto. Para desarrollo local, Alembic usará alembic.ini o el valor por defecto.
alembic upgrade head
echo "Migrations applied."

echo "Starting Uvicorn server..."
# `exec` reemplaza el shell actual con el comando uvicorn,
# lo que permite que Docker gestione correctamente las señales.
exec uvicorn app.main:app --host 0.0.0.0 --port 8080