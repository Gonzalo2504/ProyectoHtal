from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrdenMedicaSchema(BaseModel):
    id: Optional[int] = None
    id_paciente: int
    id_medico: int
    fecha_y_hora: Optional[datetime] = None
    descripcion: str
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True