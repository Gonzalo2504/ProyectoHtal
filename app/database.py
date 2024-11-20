# Importar las librerías necesarias para la base de datos
from sqlalchemy import create_engine  # Crear el motor (engine)
from sqlalchemy.ext.declarative import declarative_base  # Crear la Declarative Base
from sqlalchemy.orm import sessionmaker  # Crear la sesión de la base de datos
from .config import DATABASE_URL  # Url de la base de datos

# Crear el motor (engine)
engine = create_engine(DATABASE_URL)

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

