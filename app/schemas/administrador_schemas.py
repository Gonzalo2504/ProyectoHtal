from typing import Optional
from pydantic import BaseModel, EmailStr

class AdministradorBase(BaseModel):
    nombre: str
    apellido: str
    dni: int
    email: EmailStr
    telefono: str
    usuario: str
    contrasena: str
    rol_id: int 

class AdministradorCreate(AdministradorBase):
    pass

class AdministradorUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    usuario: Optional[str] = None
    contrasena: Optional[str] = None

class Administrador(AdministradorBase):
    id: int

    class Config:
        from_attributes = True
