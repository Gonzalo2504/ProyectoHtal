from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Schema para creación de Paciente 
class PacienteCreate(BaseModel):
    nombre: str
    apellido: str
    dni: int
    fecha_nacimiento: date
    direccion: str
    telefono: Optional[str] = None
    email: str
    estado: str
    estado_atencion: str
    triage_id : int

# Schema para mostrar los datos de Paciente
class Paciente(BaseModel):
    id: int
    nombre: str
    apellido: str
    dni: int
    fecha_nacimiento: date
    direccion: str
    telefono: Optional[str] = None
    email: str
    estado: str
    estado_atencion: str
    triage_id : int

    
    class Config:
        orm_mode = True  

class PacienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    estado: Optional[str]
    estado_atencion: Optional[str]
    triage_id : Optional[int] 

    class Config:
        orm_mode = True