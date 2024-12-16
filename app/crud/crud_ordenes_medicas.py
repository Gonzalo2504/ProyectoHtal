from app.models.models import OrdenMedica
from app.schemas.ordenesMedicas_schemas import  OrdenMedicaSchema 
from sqlalchemy.orm import Session

from app.schemas.paciente_schemas import PacienteUpdate

def create_orden_medica(db: Session, orden: OrdenMedicaSchema):
    nueva_orden = OrdenMedica(
        id_paciente=orden.id_paciente,
        id_medico=orden.id_medico,
        fecha_y_hora=orden.fecha_y_hora,
        descripcion=orden.descripcion,
        observaciones=orden.observaciones,
    )
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)

    # Actualizar el estado del paciente a "En Atención"
    paciente_update = PacienteUpdate(estado_atencion="Orden Medica Creada")
    from app.crud.crud_pacientes import update_paciente
    update_paciente(db, orden.id_paciente, paciente_update)

    return nueva_orden

def read_ordenes_medicas(db: Session, skip: int = 0, limit: int = 10):
    ordenes = db.query(OrdenMedicaSchema).offset(skip).limit(limit).all()
    return ordenes

def read_orden_medica(db: Session, orden_id: int):
    orden = db.query(OrdenMedicaSchema).filter(OrdenMedicaSchema.id == orden_id).first()
    return orden

def update_orden_medica(db: Session, orden_id: int, orden_update: OrdenMedicaSchema):
    orden = db.query(OrdenMedicaSchema).filter(OrdenMedicaSchema.id == orden_id).first()
    if orden is None:
        raise ValueError("Orden no encontrada")
    
    for key, value in orden_update.model_dump().items():
        setattr(orden, key, value)
    
    db.commit()
    db.refresh(orden)
    return orden

def delete_orden_medica(db: Session, orden_id: int):
    orden = db.query(OrdenMedicaSchema).filter(OrdenMedicaSchema.id == orden_id).first()
    if orden is None:
        raise ValueError("Orden no encontrada")
    
    db.delete(orden)
    db.commit()
    return orden

def get_ultima_orden_medica_por_paciente(db: Session, id_paciente: int):
    orden = db.query(OrdenMedica).filter(OrdenMedica.id_paciente == id_paciente).order_by(OrdenMedica.fecha_y_hora.desc()).first()
    return orden
