from pydantic import BaseModel

class AdministradorBase(BaseModel):
    nombre: str
    apellido: str
    dni: int
    email: str
    telefono: str
    usuario: str
    contrasena: str
    rol_id: int 

class AdministradorCreate(AdministradorBase):
    pass

class AdministradorUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    email: str | None = None
    telefono: str | None = None
    usuario: str | None = None
    contrasena: str | None = None

class Administrador(AdministradorBase):
    id: int

    class Config:
        orm_mode = True
