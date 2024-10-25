from typing import List
from sqlalchemy.orm import Session
from app.models import models
from app.schemas.enfermero_schemas import EnfermeroCreate, EnfermeroUpdate
from app.auth import get_password_hash

#Crud crear enfermero
def create_enfermero(db: Session, enfermero: EnfermeroCreate):
    # Hash de la contraseña
    hashed_password = get_password_hash(enfermero.contrasena)
    
    # Crear el objeto Enfermero
    db_enfermero = models.Enfermero(
        nombre=enfermero.nombre,
        apellido=enfermero.apellido,
        dni=enfermero.dni,
        email=enfermero.email,
        telefono=enfermero.telefono,
        usuario=enfermero.usuario,
        contrasena=hashed_password,
        rol_id=3
    )
    
    # Agregar el nuevo enfermero a la base de datos
    db.add(db_enfermero)
    db.commit()
    db.refresh(db_enfermero)
    return db_enfermero

def create_enfermeros(db: Session, enfermeros: List[EnfermeroCreate]):
    db_enfermeros = []
    for enfermero in enfermeros:
        # Hash de la contraseña
        hashed_password = get_password_hash(enfermero.contrasena)
        # Crear el objeto Enfermero
        db_enfermero = models.Enfermero(
            nombre=enfermero.nombre,
            apellido=enfermero.apellido,
            dni=enfermero.dni,
            email=enfermero.email,
            telefono=enfermero.telefono,
            usuario=enfermero.usuario,
            contrasena=hashed_password,
            rol_id=3
        )
        # Agregar el nuevo enfermero a la base de datos
        db.add(db_enfermero)
        db_enfermeros.append(db_enfermero)
    
    db.commit()
    for db_enfermero in db_enfermeros:
        db.refresh(db_enfermero)
    return db_enfermeros

# Obtener la lista de enfermeros
def get_enfermeros(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Enfermero).offset(skip).limit(limit).all()

# Obtener un enfermero por ID
def get_enfermero(db: Session, enfermero_id: int):
    return db.query(models.Enfermero).filter(models.Enfermero.id == enfermero_id).first()

# Actualizar los datos de un enfermero trae por id
def update_enfermero(db: Session, enfermero_id: int, enfermero: EnfermeroUpdate):
    db_enfermero = db.query(models.Enfermero).filter(models.Enfermero.id == enfermero_id).first()
    if db_enfermero:
        for key, value in enfermero.dict(exclude_unset=True).items():
            setattr(db_enfermero, key, value)
        db.commit()
        db.refresh(db_enfermero)
    return db_enfermero

# Eliminar un enfermero por ID
def delete_enfermero(db: Session, enfermero_id: int):
    db_enfermero = db.query(models.Enfermero).filter(models.Enfermero.id == enfermero_id).first()
    if db_enfermero:
        db.delete(db_enfermero)
        db.commit()
    return db_enfermero
