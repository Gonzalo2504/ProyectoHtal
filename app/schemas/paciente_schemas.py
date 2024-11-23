from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime, time

# Schema para creación de Paciente 
class PacienteCreate(BaseModel):
    nombre: str
    apellido: str
    dni: int
    fecha_nacimiento: date
    direccion: str
    telefono: Optional[str] = None
    email: EmailStr
    estado_atencion: Optional[str] = None
    fecha_estado_cambio: Optional[time] = None

# Schema para mostrar los datos de Paciente
class Paciente(BaseModel):
    id: int
    nombre: str
    apellido: str
    dni: int
    fecha_nacimiento: date
    direccion: str
    telefono: Optional[str] = None
    email: EmailStr
    estado_atencion: Optional[str] = None
    fecha_estado_cambio: Optional[time] = None
    
    class Config:
        from_attributes = True  

class PacienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    estado_atencion: Optional[str]
    fecha_estado_cambio: Optional[time] = None

    class Config:
        from_attributes = True