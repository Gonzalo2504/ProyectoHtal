from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_pacientes
from app.schemas.paciente_schemas import Paciente, PacienteCreate, PacienteUpdate
from app.database import get_db
from app.auth import get_user_by_role, Usuario

router = APIRouter()

# Ruta para crear paciente, solo accesible para administradores
@router.post("/pacientes", response_model=Paciente)
def create_paciente(paciente: PacienteCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_pacientes.create_paciente(db=db, paciente=paciente)

# Ruta para crear varios pacientes, solo accesible para administradores
@router.post("/pacientes/varios", response_model=List[Paciente])
def create_pacientes(pacientes: List[PacienteCreate], db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_pacientes.create_pacientes(db=db, pacientes=pacientes)

# Ruta para leer pacientes, accesible para administradores, enfermeros, medicos
@router.get("/pacientes", response_model=List[Paciente])
def read_pacientes(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    return crud_pacientes.get_pacientes(db=db, skip=skip, limit=limit)

# Ruta para leer un paciente específico, accesible para administradores, enfermeros, medicos
@router.get("/pacientes/{paciente_id}", response_model=Paciente)
def read_paciente(paciente_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    paciente = crud_pacientes.get_paciente(db=db, paciente_id=paciente_id)
    if paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

# Ruta para actualizar un paciente, accesible para administradores y médicos
@router.put("/pacientes/{paciente_id}", response_model=Paciente)
def update_paciente_route(paciente_id: int, paciente: PacienteUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2]))):
    db_paciente = crud_pacientes.update_paciente(db, paciente_id, paciente)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente

# Ruta para eliminar un paciente, solo accesible para administradores
@router.delete("/pacientes/{paciente_id}")
def delete_paciente_route(paciente_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    success = crud_pacientes.delete_paciente(db, paciente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"message": "Paciente eliminado exitosamente"}
