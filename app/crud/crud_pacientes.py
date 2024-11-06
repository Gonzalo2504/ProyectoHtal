from typing import List
from sqlalchemy.orm import Session
from app.models.models import Paciente as PacienteModel
from app.schemas.paciente_schemas import PacienteCreate, PacienteUpdate

# Crear un nuevo paciente
def create_paciente(db: Session, paciente: PacienteCreate):
    db_paciente = PacienteModel(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# Crear varios pacientes a la vez
def create_pacientes(db: Session, pacientes: List[PacienteCreate]):
    db_pacientes = [PacienteModel(**paciente.model_dump()) for paciente in pacientes]
    db.add_all(db_pacientes)
    db.commit()
    for paciente in db_pacientes:
        db.refresh(paciente)
    return db_pacientes

# Obtener la lista de pacientes
def get_pacientes(db: Session, skip: int = 0, limit: int = 100000):
    return db.query(PacienteModel).offset(skip).limit(limit).all()

# Obtener un paciente por ID
def get_paciente(db: Session, paciente_id: int):
    return db.query(PacienteModel).filter(PacienteModel.id == paciente_id).first()

# Actualizar datos de un paciente
def update_paciente(db: Session, paciente_id: int, paciente: PacienteUpdate):
    db_paciente = db.query(PacienteModel).filter(PacienteModel.id == paciente_id).first()
    
    if db_paciente:
        for key, value in paciente.model_dump(exclude_unset=True).items():
            setattr(db_paciente, key, value)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    return None

#Borrar un paciente
def delete_paciente(db: Session, paciente_id: int):
    db_paciente = db.query(PacienteModel).filter(PacienteModel.id == paciente_id).first()
    
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
        return True
    return False