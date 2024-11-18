# Base de la imagen
FROM python:3.10-slim

# Configuración de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear y definir el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (incluyendo libpq-dev para psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear un usuario no root
RUN useradd -m appuser
USER appuser

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto y ejecutar la aplicación
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
