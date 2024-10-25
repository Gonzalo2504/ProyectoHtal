from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_enfermeros
from app.schemas.enfermero_schemas import Enfermero, EnfermeroCreate, EnfermeroUpdate
from app.database import get_db
from app.auth import get_user_by_role, Usuario

router = APIRouter()

# Crear un nuevo enfermero, accesible para administradores
@router.post("/enfermeros/", response_model=Enfermero)
def create_enfermero(enfermero: EnfermeroCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_enfermeros.create_enfermero(db=db, enfermero=enfermero)

# Crear varios enfermeros, accesible para administradores
@router.post("/enfermeros/varios", response_model=List[Enfermero])
def create_enfermeros(enfermeros: List[EnfermeroCreate], db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_enfermeros.create_enfermeros(db=db, enfermeros=enfermeros)

# Obtener la lista de enfermeros, accesible para administradores y medicos
@router.get("/enfermeros/", response_model=List[Enfermero])
def read_enfermeros(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2]))):
    return crud_enfermeros.get_enfermeros(db=db, skip=skip, limit=limit)

# Obtener un enfermero por ID, accesible para administradores y medicos
@router.get("/enfermeros/{enfermero_id}", response_model=Enfermero)
def read_enfermero(enfermero_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2]))):
    db_enfermero = crud_enfermeros.get_enfermero(db=db, enfermero_id=enfermero_id)
    if db_enfermero is None:
        raise HTTPException(status_code=404, detail="Enfermero no encontrado")
    return db_enfermero

# Actualizar los datos de un enfermero, accesible para administradores
@router.put("/enfermeros/{enfermero_id}", response_model=Enfermero)
def update_enfermero(enfermero_id: int, enfermero: EnfermeroUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_enfermeros.update_enfermero(db=db, enfermero_id=enfermero_id, enfermero=enfermero)

# Eliminar un enfermero por ID, accesible para administradores
@router.delete("/enfermeros/{enfermero_id}", response_model=Enfermero)
def delete_enfermero(enfermero_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    db_enfermero = crud_enfermeros.delete_enfermero(db=db, enfermero_id=enfermero_id)
    if db_enfermero is None:
        raise HTTPException(status_code=404, detail="Enfermero no encontrado")
    return db_enfermero
