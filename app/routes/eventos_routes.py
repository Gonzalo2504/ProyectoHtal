from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.eventos_schemas import EventoSchema, EventoCreateSchema, EventoUpdateSchema
from app.crud.crud_eventos import get_evento, get_eventos, update_evento, delete_evento
from app.crud.crud_eventos import create_evento as crud_create_evento
from app.database import get_db
from app.auth import get_user_by_role, Usuario

router = APIRouter()

@router.get("/eventos/", response_model=list[EventoSchema])
def read_eventos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    return get_eventos(db)

@router.get("/eventos/{evento_id}", response_model=EventoSchema)
def read_evento(evento_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    db_evento = get_evento(db, evento_id)
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return db_evento

@router.post("/eventos/", response_model=EventoSchema)
def create_evento(evento: EventoCreateSchema, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2]))):
    return crud_create_evento(db, evento)

@router.put("/eventos/{evento_id}", response_model=EventoSchema)
def update_evento(evento_id: int, evento: EventoUpdateSchema, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2]))):
    db_evento = get_evento(db, evento_id)
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return update_evento(db, evento_id, evento)

@router.delete("/eventos/{evento_id}")
def delete_evento(evento_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2]))):
    db_evento = get_evento(db, evento_id)
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return delete_evento(db, evento_id)
