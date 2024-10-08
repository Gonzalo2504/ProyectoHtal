from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_administradores
from app.schemas.administrador_schemas import Administrador, AdministradorCreate, AdministradorUpdate
from app.database import get_db
from app.auth import get_user_by_role, Usuario

router = APIRouter()

# Crear un nuevo administrador, accesible para administradores
@router.post("/administradores/", response_model=Administrador)
def create_administrador(administrador: AdministradorCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_administradores.create_administrador(db=db, administrador=administrador)

# Obtener la lista de administradores, accesible para administradores
@router.get("/administradores/", response_model=List[Administrador])
def read_administradores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_administradores.get_administradores(db=db, skip=skip, limit=limit)

# Obtener un Administrador por ID, accesible para administradores
@router.get("/administradores/{administrador_id}", response_model=Administrador)
def read_administrador(administrador_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    db_administrador = crud_administradores.get_administrador(db=db, administrador_id=administrador_id)
    if db_administrador is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return db_administrador

# Actualizar los datos de un Administrador, accesible para administradores
@router.put("/administradores/{administrador_id}", response_model=Administrador)
def update_administrador(administrador_id: int, administrador: AdministradorUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_administradores.update_administrador(db=db, administrador_id=administrador_id, administrador=administrador)

# Eliminar un Administrador por ID, accesible para administradores
@router.delete("/administradores/{administrador_id}", response_model=Administrador)
def delete_administrador(administrador_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    db_administrador = crud_administradores.delete_administrador(db=db, administrador_id=administrador_id)
    if db_administrador is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return db_administrador
