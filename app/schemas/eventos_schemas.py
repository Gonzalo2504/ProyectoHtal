from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventoSchema(BaseModel):
    id: int
    tipo_evento: str
    fecha_hora: datetime
    observaciones: str
    paciente_id: int
    medico_id: Optional[int]

class EventoCreateSchema(BaseModel):
    tipo_evento: str
    fecha_hora: datetime
    observaciones: str
    paciente_id: int
    medico_id: Optional[int]

class EventoUpdateSchema(BaseModel):
    tipo_evento: Optional[str]
    fecha_hora: Optional[datetime]
    observaciones: Optional[str]
    paciente_id: Optional[int]
    medico_id: Optional[int]