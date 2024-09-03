from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_pacientes
from app.schemas.paciente_schemas import Paciente, PacienteCreate, PacienteUpdate
from app.database import get_db
from app.auth import get_current_user, get_current_medico_user, get_current_admin_user, get_current_enfermero_user, Usuario

router = APIRouter()

@router.post("/pacientes/", response_model=Paciente)
def create_paciente(paciente: PacienteCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin_user)):
    return crud_pacientes.create_paciente(db=db, paciente=paciente)

@router.get("/pacientes/", response_model=List[Paciente])
def read_pacientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return crud_pacientes.get_pacientes(db=db, skip=skip, limit=limit)

@router.get("/pacientes/{paciente_id}", response_model=Paciente)
def read_paciente(paciente_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    paciente = crud_pacientes.get_paciente(db=db, paciente_id=paciente_id)
    if paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.put("/pacientes/{paciente_id}", response_model=Paciente)
def update_paciente_route(paciente_id: int, paciente: PacienteUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin_user or get_current_medico_user)):
    db_paciente = crud_pacientes.update_paciente(db, paciente_id, paciente)
    
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    return db_paciente

@router.delete("/pacientes/{paciente_id}")
def delete_paciente_route(paciente_id: int, db: Session = Depends(get_db), current_user : Usuario = Depends(get_current_admin_user)):
    success = crud_pacientes.delete_paciente(db, paciente_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    return {"message": "Paciente eliminado exitosamente"}