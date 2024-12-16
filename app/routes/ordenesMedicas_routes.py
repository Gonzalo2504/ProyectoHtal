from fastapi import APIRouter, Depends, HTTPException
from app.crud.crud_ordenes_medicas import create_orden_medica, read_ordenes_medicas, read_orden_medica, update_orden_medica, delete_orden_medica, get_ultima_orden_medica_por_paciente
from app.auth import get_user_by_role, Usuario
from app.schemas.ordenesMedicas_schemas import OrdenMedicaSchema
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

router = APIRouter()

# Crear una nueva orden médica
@router.post("/ordenes_medicas/", response_model=OrdenMedicaSchema)
def create_orden_medica_endpoint(orden: OrdenMedicaSchema, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2]))):
    return create_orden_medica(db, orden)

# Leer todas las órdenes médicas
@router.get("/ordenes_medicas/", response_model=List[OrdenMedicaSchema])
def read_ordenes_medicas_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    return read_ordenes_medicas(db, skip, limit)

# Leer una orden médica específica por su ID
@router.get("/ordenes_medicas/{orden_id}", response_model=OrdenMedicaSchema)
def read_orden_medica_endpoint(orden_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    orden = read_orden_medica(db, orden_id)
    if orden is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return orden

# Leer la última orden médica de un paciente por su ID
@router.get("/ordenes_medicas/ultima_por_paciente/{id_paciente}", response_model=OrdenMedicaSchema)
def get_ultima_orden_medica_por_paciente_endpoint(id_paciente: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    orden = get_ultima_orden_medica_por_paciente(db, id_paciente)
    if orden is None:
        raise HTTPException(status_code=404, detail="No se encontró la orden")
    return orden

# Actualizar una orden médica por su ID
@router.put("/ordenes_medicas/{orden_id}", response_model=OrdenMedicaSchema)
def update_orden_medica_endpoint(orden_id: int, orden_update: OrdenMedicaSchema, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2]))):
    try:
        return update_orden_medica(db, orden_id, orden_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Eliminar una orden médica por su ID
@router.delete("/ordenes_medicas/{orden_id}", response_model=OrdenMedicaSchema)
def delete_orden_medica_endpoint(orden_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2]))):
    try:
        return delete_orden_medica(db, orden_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))