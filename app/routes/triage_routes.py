from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_triage
from app.schemas.triage_schemas import TriageCreate, TriageRead, TriageUpdate, TriageList
from app.database import get_db
from app.auth import get_user_by_role, Usuario

router = APIRouter()

# Crear un nuevo Triage, accesible para enfermeros
@router.post("/triages/", response_model=TriageRead)
def create_triage(triage: TriageCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([3]))):
    return crud_triage.create_triage(db=db, triage=triage)

# Obtener un Triage por ID, , accesible para administradores, enfermeros y medicos
@router.get("/triages/{triage_id}", response_model=TriageRead)
def read_triage(triage_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    db_triage = crud_triage.get_triage(db=db, triage_id=triage_id)
    if db_triage is None:
        raise HTTPException(status_code=404, detail="Triage no encontrado")
    return db_triage

# Obtener una lista de todos los Triages (con paginación)
@router.get("/triages/", response_model=List[TriageRead])
def read_triages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([3]))):
    return crud_triage.get_triages(db=db, skip=skip, limit=limit)

# Actualizar un Triage por ID
@router.put("/triages/{triage_id}", response_model=TriageRead)
def update_triage(triage_id: int, triage: TriageUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([3]))):
    db_triage = crud_triage.update_triage(db=db, triage_id=triage_id, triage=triage)
    if db_triage is None:
        raise HTTPException(status_code=404, detail="Triage no encontrado")
    return db_triage

# Eliminar un Triage por ID, accesible para administradores y enfermeros
@router.delete("/triages/{triage_id}", response_model=TriageRead)
def delete_triage(triage_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 3]))):
    db_triage = crud_triage.delete_triage(db=db, triage_id=triage_id)
    if db_triage is None:
        raise HTTPException(status_code=404, detail="Triage no encontrado")
    return db_triage
