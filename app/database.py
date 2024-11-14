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

# Función para obtener la sesión de la base de datos
# Esta función utiliza un yield para que se pueda utilizar como un contexto
# en un with, y se encargue de cerrar la sesión al finalizar
def get_db():
    db = SessionLocal()
    try:
        # El yield devuelve el objeto db, que es la sesión de la base de datos
        # y se puede utilizar dentro del contexto
        yield db
    finally:
        # Al finalizar el contexto, se cierra la sesión
        db.close()

