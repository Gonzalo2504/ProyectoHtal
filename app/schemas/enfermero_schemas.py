from pydantic import BaseModel

class EnfermeroBase(BaseModel):
    nombre: str
    apellido: str
    dni: int
    email: str
    telefono: str
    usuario: str
    contrasena: str
    rol_id: int 

class EnfermeroCreate(EnfermeroBase):
    pass

class EnfermeroUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    dni: int | None = None
    email: str | None = None
    telefono: str | None = None
    usuario: str | None = None
    contrasena: str | None = None

class Enfermero(EnfermeroBase):
    id: int

    class Config:
        from_attributes = True
