from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import OrdenMedica
from app.schemas.ordenesMedicas_schemas import OrdenMedicaCreate, OrdenMedica as OrdenMedicaSchema
from app.database import get_db
from app.auth import get_user_by_role, Usuario


router = APIRouter()

# Crear una nueva orden médica
@router.post("/ordenes_medicas/", response_model=OrdenMedicaSchema)
def create_orden_medica(orden: OrdenMedicaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2]))):
    nueva_orden = OrdenMedica(**orden.model_dump())
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)
    return nueva_orden

# Leer todas las órdenes médicas
@router.get("/ordenes_medicas/", response_model=List[OrdenMedicaSchema])
def read_ordenes_medicas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    ordenes = db.query(OrdenMedica).offset(skip).limit(limit).all()
    return ordenes

# Leer una orden médica específica por su ID
@router.get("/ordenes_medicas/{orden_id}", response_model=OrdenMedicaSchema)
def read_orden_medica(orden_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    orden = db.query(OrdenMedica).filter(OrdenMedica.id == orden_id).first()
    if orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return orden

# Actualizar una orden médica por su ID
@router.put("/ordenes_medicas/{orden_id}", response_model=OrdenMedicaSchema)
def update_orden_medica(orden_id: int, orden_update: OrdenMedicaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2]))):
    orden = db.query(OrdenMedica).filter(OrdenMedica.id == orden_id).first()
    if orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    for key, value in orden_update.model_dump().items():
        setattr(orden, key, value)
    
    db.commit()
    db.refresh(orden)
    return orden

# Eliminar una orden médica por su ID
@router.delete("/ordenes_medicas/{orden_id}", response_model=OrdenMedicaSchema)
def delete_orden_medica(orden_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2]))):
    orden = db.query(OrdenMedica).filter(OrdenMedica.id == orden_id).first()
    if orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    db.delete(orden)
    db.commit()
    return orden
