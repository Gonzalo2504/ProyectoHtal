from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.evolucionPaciente_schemas import EvolucionPacienteCreate, EvolucionPacienteUpdate, EvolucionPacienteRead
from app.crud import crud_evoluciones as evolucion_paciente_crud
from app.auth import get_user_by_role, Usuario

router = APIRouter()

@router.post("/evolucion_paciente/", response_model=EvolucionPacienteRead)
def create_evolucion_paciente(evolucion_paciente: EvolucionPacienteCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([3]))):
    return evolucion_paciente_crud.create_evolucion_paciente(db, evolucion_paciente)

@router.get("/evolucion_paciente/{id}", response_model=EvolucionPacienteRead)
def read_evolucion_paciente(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1, 2, 3]))):
    evolucion_paciente = evolucion_paciente_crud.get_evolucion_paciente(db, id)
    if not evolucion_paciente:
        raise HTTPException(status_code=404, detail="Evolución de paciente no encontrada")
    return evolucion_paciente

@router.put("/evolucion_paciente/{id}", response_model=EvolucionPacienteRead)
def update_evolucion_paciente(id: int, evolucion_paciente: EvolucionPacienteUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([3]))):
    evolucion_paciente_db = evolucion_paciente_crud.get_evolucion_paciente(db, id)
    if not evolucion_paciente_db:
        raise HTTPException(status_code=404, detail="Evolución de paciente no encontrada")
    return evolucion_paciente_crud.update_evolucion_paciente(db, evolucion_paciente_db, evolucion_paciente)

@router.delete("/evolucion_paciente/{id}")
def delete_evolucion_paciente(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1,3]))):
    evolucion_paciente_db = evolucion_paciente_crud.get_evolucion_paciente(db, id)
    if not evolucion_paciente_db:
        raise HTTPException(status_code=404, detail="Evolución de paciente no encontrada")
    evolucion_paciente_crud.delete_evolucion_paciente(db, evolucion_paciente_db)
    return {"message": "Evolución de paciente eliminada"}
