from app.models.models import OrdenMedica
from app.schemas.ordenesMedicas_schemas import OrdenMedicaCreate, OrdenMedica 
from sqlalchemy.orm import Session

def create_orden_medica(db: Session, orden: OrdenMedicaCreate):
    nueva_orden = OrdenMedica(**orden.model_dump())
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)
    return nueva_orden

def read_ordenes_medicas(db: Session, skip: int = 0, limit: int = 10):
    ordenes = db.query(OrdenMedica).offset(skip).limit(limit).all()
    return ordenes

def read_orden_medica(db: Session, orden_id: int):
    orden = db.query(OrdenMedica).filter(OrdenMedica.id == orden_id).first()
    return orden

def update_orden_medica(db: Session, orden_id: int, orden_update: OrdenMedicaCreate):
    orden = db.query(OrdenMedica).filter(OrdenMedica.id == orden_id).first()
    if orden is None:
        raise ValueError("Orden no encontrada")
    
    for key, value in orden_update.model_dump().items():
        setattr(orden, key, value)
    
    db.commit()
    db.refresh(orden)
    return orden

def delete_orden_medica(db: Session, orden_id: int):
    orden = db.query(OrdenMedica).filter(OrdenMedica.id == orden_id).first()
    if orden is None:
        raise ValueError("Orden no encontrada")
    
    db.delete(orden)
    db.commit()
    return orden