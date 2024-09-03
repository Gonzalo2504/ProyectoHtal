from pydantic import BaseModel
from typing import Optional

class MedicoBase(BaseModel):
    nombre: str
    apellido: str
    dni: int
    especialidad: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    usuario: Optional[str] = None
    contrasena: Optional[str] = None
    rol_id: int 

class MedicoCreate(MedicoBase):
    pass

class MedicoUpdate(MedicoBase):
    pass

class Medico(MedicoBase):
    id: int

    class Config:
        from_attributes = True
