from typing import Optional
from pydantic import BaseModel, EmailStr

class EnfermeroBase(BaseModel):
    nombre: str
    apellido: str
    dni: int
    email: EmailStr
    telefono: str
    usuario: str
    contrasena: str
    rol_id: int 

class EnfermeroCreate(EnfermeroBase):
    pass

class EnfermeroUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[int] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    usuario: Optional[str] = None
    contrasena: Optional[str] = None

class Enfermero(EnfermeroBase):
    id: int

    class Config:
        from_attributes = True
