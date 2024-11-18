from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

# Define la URL de conexión a la base de datos basada en la configuración del contenedor
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://user:password@db:5432/thor_database"  # URL de la base de datos del docker-compose.yml
)

# Crea el motor de conexión a la base de datos
engine = create_engine(DATABASE_URL)

# Crea una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir modelos de SQLAlchemy
Base = declarative_base()


