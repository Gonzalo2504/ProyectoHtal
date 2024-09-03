from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_medicos
from app.schemas.medico_schemas import Medico, MedicoCreate, MedicoUpdate
from app.database import get_db
from app.auth import get_current_user, get_current_medico_user, get_current_admin_user, get_current_enfermero_user, Usuario

router = APIRouter()

# Crear un nuevo medico
@router.post("/medicos/", response_model=Medico)
def create_medico(medico: MedicoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin_user)):
    return crud_medicos.create_medico(db=db, medico=medico)

@router.get("/medicos/", response_model=List[Medico])
def read_medicos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),  current_user: Usuario = Depends(get_current_admin_user)):
    return crud_medicos.get_medicos(db=db, skip=skip, limit=limit)

@router.get("/medicos/{medico_id}", response_model=Medico)
def read_medico(medico_id: int, db: Session = Depends(get_db),  current_user: Usuario = Depends(get_current_admin_user)):
    db_medico = crud_medicos.get_medico(db=db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Medico no encontrado")
    return db_medico

@router.put("/medicos/{medico_id}", response_model=Medico)
def update_medico(medico_id: int, medico: MedicoUpdate, db: Session = Depends(get_db),  current_user: Usuario = Depends(get_current_admin_user or get_current_medico_user)):
    db_medico = crud_medicos.update_medico(db=db, medico_id=medico_id, medico=medico)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Medico no encontrado")
    return db_medico

@router.delete("/medicos/{medico_id}", response_model=Medico)
def delete_medico(medico_id: int, db: Session = Depends(get_db),  current_user: Usuario = Depends(get_current_admin_user)):
    db_medico = crud_medicos.delete_medico(db=db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Medico no encontrado")
    return db_medico
