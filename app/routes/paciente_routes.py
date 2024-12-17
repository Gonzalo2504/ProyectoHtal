from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import crud_pacientes, crud_triage
from app.schemas.paciente_schemas import Paciente, PacienteCreate, PacienteUpdate
from app.schemas.evolucionPaciente_schemas import EvolucionPacienteRead
from app.schemas.triage_schemas import TriageRead
from app.models.models import EvolucionPaciente, TriagePaciente
from app.database import get_db
from app.auth import get_user_by_role, Usuario

router = APIRouter()

# Ruta para crear paciente, solo accesible para administradores
@router.post("/pacientes", response_model=Paciente)
def create_paciente(paciente: PacienteCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_pacientes.create_paciente(db=db, paciente=paciente)

# Ruta para crear varios pacientes, solo accesible para administradores
@router.post("/pacientes/varios", response_model=List[Paciente])
def create_pacientes(pacientes: List[PacienteCreate], db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    return crud_pacientes.create_pacientes(db=db, pacientes=pacientes)

# Ruta para leer pacientes, accesible para administradores, enfermeros, medicos
@router.get("/pacientes", response_model=List[Paciente])
def read_pacientes(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    return crud_pacientes.get_pacientes(db=db, skip=skip, limit=limit)

# Ruta para leer un paciente específico, accesible para administradores, enfermeros, medicos
@router.get("/pacientes/{paciente_id}", response_model=Paciente)
def read_paciente(paciente_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    paciente = crud_pacientes.get_paciente(db=db, paciente_id=paciente_id)
    if paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

# Ruta para actualizar un paciente, accesible para administradores y médicos
@router.put("/pacientes/{paciente_id}", response_model=Paciente)
def update_paciente_route(paciente_id: int, paciente: PacienteUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2]))):
    db_paciente = crud_pacientes.update_paciente(db, paciente_id, paciente)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente

# Ruta para eliminar un paciente, solo accesible para administradores
@router.delete("/pacientes/{paciente_id}")
def delete_paciente_route(paciente_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    success = crud_pacientes.delete_paciente(db, paciente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"message": "Paciente eliminado exitosamente"}

# Ruta para leer pacientes en espera, accesible para enfermeros
@router.get("/pacientes/en_espera/lista", response_model=List[Paciente])
def read_pacientes_en_espera(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([3]))):
    return crud_pacientes.get_pacientes_en_espera(db=db, skip=skip, limit=limit)

# Ruta para leer pacientes atendidos, accesible para enfermeros
@router.get("/pacientes/atendidos/lista", response_model=List[Paciente])
def read_pacientes_atendidos(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([3]))):
    return crud_pacientes.get_pacientes_atendidos(db=db, skip=skip, limit=limit)

# Ruta para leer pacientes en tratamiento, accesible para enfermeros
@router.get("/pacientes/en_tratamiento/lista", response_model=List[Paciente])
def read_pacientes_en_tratamiento(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([3]))):
    return crud_pacientes.get_pacientes_en_tratamiento(db=db, skip=skip, limit=limit)

# Ruta para leer pacientes con orden medica creada, accesible para enfermeros
@router.get("/pacientes/orden-medica-creada/lista", response_model=List[Paciente])
def read_pacientes_con_orden_medica_creada(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([3]))):
    return crud_pacientes.get_pacientes_con_orden_medica_creada(db=db, skip=skip, limit=limit)

# Ruta para leer pacientes con evolución de enfermería, accesible para enfermeros
@router.get("/pacientes/con-evolucion-de-enfermeria/lista", response_model=List[Paciente])
def read_pacientes_con_evolucion_de_enfermeria(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2, 3]))):
    return crud_pacientes.get_pacientes_con_evolucion_de_enfermeria(db=db, skip=skip, limit=limit)

@router.get("/pacientes/{paciente_id}/ultima-evolucion", response_model=EvolucionPacienteRead)
def get_ultima_evolucion(paciente_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2]))):
    ultima_evolucion = db.query(EvolucionPaciente).filter(EvolucionPaciente.id_paciente == paciente_id).order_by(EvolucionPaciente.fecha_y_hora.desc()).first()
    return ultima_evolucion

# Ruta para leer pacientes por clasificación, accesible para medicos
@router.get("/pacientes/en-atencion/clasificacion/{clasificacion}", response_model=list[Paciente])
def listar_pacientes_por_triaje(clasificacion: str, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2]))):
    return crud_triage.obtener_pacientes_por_clasificacion_y_estado(db, clasificacion)

# Obtener último triage de un paciente
@router.get("/pacientes/{paciente_id}/ultimo-triage", response_model=TriageRead)
def get_ultimo_triage(paciente_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([2]))):
    ultimo_triage = db.query(TriagePaciente).filter(TriagePaciente.id_paciente == paciente_id).order_by(TriagePaciente.fecha_y_hora.desc()).first()
    return ultimo_triage
