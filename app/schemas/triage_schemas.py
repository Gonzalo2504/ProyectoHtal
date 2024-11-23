from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# POST: Crear un nuevo Triage
class TriageCreate(BaseModel):
    id_paciente: int
    id_enfermero: int
    fecha_y_hora: Optional[datetime] = None
    clasificacion: str
    antecedentes: Optional[str] = None
    frecuencia_cardiaca: Optional[str] = None
    presion_arterial_sistolica: Optional[str] = None
    presion_arterial_diastolica: Optional[str] = None
    temperatura: Optional[str] = None
    frecuencia_respiratoria: Optional[str] = None
    saturacion_oxigeno: Optional[str] = None
    motivo_consulta: Optional[str] = None
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True

# GET: Leer un Triage
class TriageRead(BaseModel):
    id_triage: int
    id_paciente: int
    id_enfermero: int
    fecha_y_hora: datetime
    clasificacion: str
    antecedentes: Optional[str] = None
    frecuencia_cardiaca: Optional[str] = None
    presion_arterial_sistolica: Optional[str] = None
    presion_arterial_diastolica: Optional[str] = None
    temperatura: Optional[str] = None
    frecuencia_respiratoria: Optional[str] = None
    saturacion_oxigeno: Optional[str] = None
    motivo_consulta: Optional[str] = None
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True

# PUT: Actualizar un Triage
class TriageUpdate(BaseModel):
    clasificacion: Optional[str] = None
    antecedentes: Optional[str] = None
    frecuencia_cardiaca: Optional[str] = None
    presion_arterial_sistolica: Optional[str] = None
    presion_arterial_diastolica: Optional[str] = None
    temperatura: Optional[str] = None
    frecuencia_respiratoria: Optional[str] = None
    saturacion_oxigeno: Optional[str] = None
    motivo_consulta: Optional[str] = None
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True

# GET: Lista de Triage
class TriageList(BaseModel):
    triages: List[TriageRead]

    class Config:
        from_attributes = True
