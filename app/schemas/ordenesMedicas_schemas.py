from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema para crear una nueva orden médica
class OrdenMedicaCreate(BaseModel):
    id_paciente: int
    id_medico: int
    descripcion: str
    estado: str
    observaciones: Optional[str] = None

# Schema para leer una orden médica (incluye id y fecha)
class OrdenMedica(BaseModel):
    id: int
    id_paciente: int
    id_medico: int
    fecha_y_hora: datetime
    descripcion: str
    estado: str
    observaciones: Optional[str] = None

    class Config:
        orm_mode = True
