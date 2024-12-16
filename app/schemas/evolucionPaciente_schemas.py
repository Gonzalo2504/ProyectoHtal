from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EvolucionPacienteBase(BaseModel):
    id_orden_medica: int
    id_paciente: int
    id_enfermero: int
    descripcion: str
    fecha_y_hora: Optional[datetime]

class EvolucionPacienteCreate(EvolucionPacienteBase):
    pass

class EvolucionPacienteUpdate(EvolucionPacienteBase):
    id: Optional[int]
    id_orden_medica: Optional[int]
    id_paciente: Optional[int]
    id_enfermero: Optional[int]
    descripcion: Optional[str]
    fecha_y_hora: Optional[datetime]

class EvolucionPacienteRead(EvolucionPacienteBase):
    id: int

    class Config:
        orm_mode = True

class EvolucionPacienteDelete(BaseModel):
    id: int