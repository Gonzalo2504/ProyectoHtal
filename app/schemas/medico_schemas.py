from pydantic import BaseModel, EmailStr
from typing import Optional

class MedicoBase(BaseModel):
    nombre: str
    apellido: str
    dni: int
    especialidad: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    usuario: Optional[str] = None
    contrasena: Optional[str] = None
    rol_id: int  

class MedicoCreate(MedicoBase):
    pass

class MedicoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[int] = None
    especialidad: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    usuario: Optional[str] = None
    contrasena: Optional[str] = None
    rol_id: Optional[int] = None

class Medico(MedicoBase):
    id: int

    class Config:
        from_attributes = True
