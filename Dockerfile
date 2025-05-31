# Dockerfile
FROM python:3.12-slim-bookworm

# Evita que Python escriba archivos .pyc en el disco y buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Variables para GCP
ENV PORT=8080

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# --- Fase de Instalación de Dependencias (para mejor build caching) ---
COPY requirements.txt .

# Instalar dependencias del sistema operativo que son necesarias para compilar algunas librerías Python.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    # Agrega aquí otras dependencias del sistema si tus librerías Python las requieren, por ejemplo:
    # default-libmysqlclient-dev pkg-config  # Para mysqlclient
    # unixodbc-dev                             # Para pyodbc (SQL Server)
    # libffi-dev                               # Para algunas librerías criptográficas
    && rm -rf /var/lib/apt/lists/* # Limpiar el caché de apt para reducir el tamaño de la imagen

# Instala las dependencias de Python.
# `--no-cache-dir` para no guardar el caché de pip en el contenedor, reduciendo el tamaño final.
RUN pip install --no-cache-dir -r requirements.txt

# --- Fase de Copia de Código y Configuración de Usuario No-Root ---
# Crear un usuario no-root para ejecutar la aplicación, por motivos de seguridad.
# Usamos un UID/GID específico para consistencia y para que el usuario sea reconocido.
RUN addgroup --system appgroup && adduser --system --uid 1000 --ingroup appgroup appuser
COPY ./app /app/app

# Copia el resto del código 
COPY ./alembic /app/alembic
COPY alembic.ini /app/
COPY scripts/app.sh /usr/local/bin/app.sh


# Asegura que el script de ejecución tenga permisos ejecutables.
RUN chmod +x /usr/local/bin/app.sh


# Cambiar el propietario de los archivo
RUN chown -R appuser:appgroup /app

# Cambiar al usuario no-root. Todas las operaciones posteriores (incluyendo CMD) se ejecutarán como 'appuser'.
USER appuser

# Health check para GCP
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:$PORT/health || exit 1

# Expone el puerto en el que se ejecutará la aplicación (documentación, no abre el puerto realmente).
EXPOSE $PORT

# Comando para ejecutar la aplicación cuando se inicie el contenedor.
# El script run_app.sh se encargará de las migraciones y de iniciar el servidor.
CMD ["/usr/local/bin/app.sh"]