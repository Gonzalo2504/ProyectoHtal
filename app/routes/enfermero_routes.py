from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_enfermeros
from app.schemas.enfermero_schemas import Enfermero, EnfermeroCreate, EnfermeroUpdate
from app.database import get_db
from app.auth import get_current_user, get_current_medico_user, get_current_admin_user, get_current_enfermero_user, Usuario

router = APIRouter()

# Crear un nuevo enfermero
@router.post("/enfermeros/", response_model=Enfermero)
def create_enfermero(enfermero: EnfermeroCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin_user)):
    return crud_enfermeros.create_enfermero(db=db, enfermero=enfermero)

# Obtener la lista de enfermeros
@router.get("/enfermeros/", response_model=List[Enfermero])
def read_enfermeros(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin_user)):
    return crud_enfermeros.get_enfermeros(db=db, skip=skip, limit=limit)

# Obtener un enfermero por ID
@router.get("/enfermeros/{enfermero_id}", response_model=Enfermero)
def read_enfermero(enfermero_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin_user)):
    db_enfermero = crud_enfermeros.get_enfermero(db=db, enfermero_id=enfermero_id)
    if db_enfermero is None:
        raise HTTPException(status_code=404, detail="Enfermero no encontrado")
    return db_enfermero

# Actualizar los datos de un enfermero
@router.put("/enfermeros/{enfermero_id}", response_model=Enfermero)
def update_enfermero(enfermero_id: int, enfermero: EnfermeroUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin_user or get_current_enfermero_user)):
    return crud_enfermeros.update_enfermero(db=db, enfermero_id=enfermero_id, enfermero=enfermero)

# Eliminar un enfermero por ID
@router.delete("/enfermeros/{enfermero_id}", response_model=Enfermero)
def delete_enfermero(enfermero_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin_user)):
    db_enfermero = crud_enfermeros.delete_enfermero(db=db, enfermero_id=enfermero_id)
    if db_enfermero is None:
        raise HTTPException(status_code=404, detail="Enfermero no encontrado")
    return db_enfermero
