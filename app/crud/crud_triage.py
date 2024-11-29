from sqlalchemy.orm import Session
from app.models.models import TriagePaciente
from app.schemas.triage_schemas import TriageCreate, TriageUpdate
from app.crud import crud_pacientes
from app.schemas.paciente_schemas import PacienteUpdate

# Crear un nuevo triage
def update_estado_atencion_paciente(db: Session, paciente_id: int):
    paciente_update = PacienteUpdate(estado_atencion="En atención")
    crud_pacientes.update_paciente(db, paciente_id, paciente_update)

def create_triage(db: Session, triage: TriageCreate):
    db_triage = TriagePaciente(**triage.model_dump())
    db.add(db_triage)
    db.commit()
    db.refresh(db_triage)

    update_estado_atencion_paciente(db, triage.id_paciente)

    return db_triage

# Obtener todos los triages
def get_triages(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TriagePaciente).offset(skip).limit(limit).all()

# Obtener un triage por su ID
def get_triage(db: Session, triage_id: int):
    return db.query(TriagePaciente).filter(TriagePaciente.id_triage == triage_id).first()

# Actualizar un triage
def update_triage(db: Session, triage_id: int, triage: TriageUpdate):
    db_triage = db.query(TriagePaciente).filter(TriagePaciente.id_triage == triage_id).first()
    if db_triage:
        for key, value in triage.model_dump(exclude_unset=True).items():
            setattr(db_triage, key, value)
        db.commit()
        db.refresh(db_triage)
    return db_triage

# Eliminar un triage
def delete_triage(db: Session, triage_id: int):
    db_triage = db.query(TriagePaciente).filter(TriagePaciente.id_triage == triage_id).first()
    if db_triage:
        db.delete(db_triage)
        db.commit()
    return db_triage
