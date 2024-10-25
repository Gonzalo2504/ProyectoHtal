from typing import List
from sqlalchemy.orm import Session
from app.models.models import Medico
from app.schemas.medico_schemas import MedicoCreate, MedicoUpdate

from app.auth import get_password_hash

#Crud crear medico
def create_medico(db: Session, medico: MedicoCreate):
    # Hash de la contraseña
    hashed_password = get_password_hash(medico.contrasena)
    
    # Crear el objeto Medico
    db_medico = Medico(
        nombre=medico.nombre,
        apellido=medico.apellido,
        dni=medico.dni,
        especialidad=medico.especialidad,
        email=medico.email,
        telefono=medico.telefono,
        usuario=medico.usuario,
        contrasena=hashed_password,
        rol_id=2
    )
    
    # Agregar el nuevo medico a la base de datos
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

#Crear varios medicos
def create_medicos(db: Session, medicos: List[MedicoCreate]):
    db_medicos = []
    for medico in medicos:
        # Hash de la contraseña
        hashed_password = get_password_hash(medico.contrasena)
        # Crear el objeto Medico
        db_medico = Medico(
            nombre=medico.nombre,
            apellido=medico.apellido,
            dni=medico.dni,
            especialidad=medico.especialidad,
            email=medico.email,
            telefono=medico.telefono,
            usuario=medico.usuario,
            contrasena=hashed_password,
            rol_id=2
        )
        # Agregar el nuevo medico a la base de datos
        db.add(db_medico)
        db.commit()
        db.refresh(db_medico)
        db_medicos.append(db_medico)
    return db_medicos

#Traer medico po  id
def get_medico(db: Session, medico_id: int):
    return db.query(Medico).filter(Medico.id == medico_id).first()

#Traer todos los medicos de la BD
def get_medicos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Medico).offset(skip).limit(limit).all()

#Actualizar datos del medico de la BD, lo trae por id
def update_medico(db: Session, medico_id: int, medico: MedicoUpdate):
    db_medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if db_medico is None:
        return None

    for var, value in vars(medico).items():
        setattr(db_medico, var, value) if value else None

    db.commit()
    db.refresh(db_medico)
    return db_medico

#Borrar medico por id
def delete_medico(db: Session, medico_id: int):
    db_medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if db_medico is None:
        return None

    db.delete(db_medico)
    db.commit()
    return db_medico
