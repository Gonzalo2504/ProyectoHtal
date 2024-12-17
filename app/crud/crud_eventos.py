from sqlalchemy.orm import Session
from app.schemas.eventos_schemas import EventoSchema, EventoCreateSchema, EventoUpdateSchema
from app.models.models import Evento

def get_evento(db: Session, evento_id: int):
    return db.query(Evento).filter(Evento.id == evento_id).first()

def get_eventos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Evento).offset(skip).limit(limit).all()

def create_evento(db: Session, evento: EventoCreateSchema):
    db_evento = Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def update_evento(db: Session, evento_id: int, evento: EventoUpdateSchema):
    db_evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if db_evento is None:
        raise ValueError("Evento no encontrado")
    for field, value in evento.dict().items():
        if value is not None:
            setattr(db_evento, field, value)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def delete_evento(db: Session, evento_id: int):
    db_evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if db_evento is None:
        raise ValueError("Evento no encontrado")
    db.delete(db_evento)
    db.commit()
    return True