from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_medicos
from app.schemas.medico_schemas import Medico, MedicoCreate, MedicoUpdate
from app.database import get_db
from app.auth import get_user_by_role, Usuario

router = APIRouter()

# Crear un nuevo médico, solo accesible para administradores
@router.post("/medicos/", response_model=Medico)
def create_medico(medico: MedicoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_medicos.create_medico(db=db, medico=medico)

# Ruta para crear varios médicos, solo accesible para administradores
@router.post("/medicos/varios", response_model=List[Medico])
def create_medicos(medicos: List[MedicoCreate], db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_medicos.create_medicos(db=db, medicos=medicos)

# Leer todos los médicos, accesible para administradores y enfermeros
@router.get("/medicos/", response_model=List[Medico])
def read_medicos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 3]))):
    return crud_medicos.get_medicos(db=db, skip=skip, limit=limit)

# Leer un médico específico, accesible para administradores y enfermeros
@router.get("/medicos/{medico_id}", response_model=Medico)
def read_medico(medico_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 3]))):
    db_medico = crud_medicos.get_medico(db=db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return db_medico

# Actualizar la información de un médico, accesible para administradores
@router.put("/medicos/{medico_id}", response_model=Medico)
def update_medico(medico_id: int, medico: MedicoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    db_medico = crud_medicos.update_medico(db=db, medico_id=medico_id, medico=medico)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return db_medico

# Eliminar un médico, solo accesible para administradores
@router.delete("/medicos/{medico_id}", response_model=Medico)
def delete_medico(medico_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    db_medico = crud_medicos.delete_medico(db=db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return db_medico
