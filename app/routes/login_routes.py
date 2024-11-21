from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.auth import verify_password, create_access_token
from app.schemas.login_schemas import LoginSchema
from app.models.models import Medico, Enfermero, Administrador
from app.database import get_db

router = APIRouter()

@router.post("/login")
def login(credentials: LoginSchema, db: Session = Depends(get_db)):
    # Buscar el usuario en la tabla de médicos 
    medico = db.query(Medico).filter(Medico.usuario == credentials.usuario).first()
    enfermero = db.query(Enfermero).filter(Enfermero.usuario == credentials.usuario).first()
    administrador = db.query(Administrador).filter(Administrador.usuario == credentials.usuario).first()

    user = medico or enfermero or administrador # Validar el tipo de usuario

    if not user or not verify_password(credentials.contrasena, user.contrasena):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")

    # Crear token de acceso
    access_token = create_access_token(data={"sub": user.usuario, "id_usuario": user.id, "rol_id": user.rol_id})

    return {"access_token": access_token, "token_type": "bearer"}