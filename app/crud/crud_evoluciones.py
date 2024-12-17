from sqlalchemy.orm import Session
from app.models.models import EvolucionPaciente
from app.schemas.evolucionPaciente_schemas import EvolucionPacienteCreate, EvolucionPacienteUpdate
from app.schemas.paciente_schemas import PacienteUpdate

def create_evolucion_paciente(db: Session, evolucion_paciente: EvolucionPacienteCreate):
    evolucion_paciente_db = EvolucionPaciente(**evolucion_paciente.dict())
    db.add(evolucion_paciente_db)
    db.commit()
    db.refresh(evolucion_paciente_db)

    # Actualizar el estado del paciente a "En Atención"
    paciente_update = PacienteUpdate(estado_atencion="Con Evolucion de Enfermeria")
    from app.crud.crud_pacientes import update_paciente
    update_paciente(db, evolucion_paciente.id_paciente, paciente_update)

    return evolucion_paciente_db

def get_evolucion_paciente(db: Session, id: int):
    return db.query(EvolucionPaciente).filter(EvolucionPaciente.id == id).first()

def update_evolucion_paciente(db: Session, evolucion_paciente_db: EvolucionPaciente, evolucion_paciente: EvolucionPacienteUpdate):
    evolucion_paciente_db.id_orden_medica = evolucion_paciente.id_orden_medica
    evolucion_paciente_db.id_paciente = evolucion_paciente.id_paciente
    evolucion_paciente_db.id_enfermero = evolucion_paciente.id_enfermero
    evolucion_paciente_db.descripcion = evolucion_paciente.descripcion
    evolucion_paciente_db.fecha_y_hora = evolucion_paciente.fecha_y_hora
    db.commit()
    db.refresh(evolucion_paciente_db)
    return evolucion_paciente_db

def delete_evolucion_paciente(db: Session, evolucion_paciente_db: EvolucionPaciente):
    db.delete(evolucion_paciente_db)
    db.commit()