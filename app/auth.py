from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE
from app.models.models import Administrador, Medico, Enfermero
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from typing import Union

# Define el esquema para extraer el token de la cabecera "Authorization"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password_plano, hashed_password):
    return pwd_context.verify(password_plano, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        rol_id: int = payload.get("rol_id")
        if usuario is None or rol_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Buscar el usuario en la base de datos según su rol y nombre de usuario
    if rol_id == 1:  # Administrador
        user = db.query(Administrador).filter(Administrador.usuario == usuario).first()
    elif rol_id == 2:  # Médico
        user = db.query(Medico).filter(Medico.usuario == usuario).first()
    elif rol_id == 3:  # Enfermero
        user = db.query(Enfermero).filter(Enfermero.usuario == usuario).first()
    else:
        raise credentials_exception
    
    if user is None:
        raise credentials_exception
    
    return user

Usuario = Union[Medico, Administrador, Enfermero]

def get_current_admin_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.rol_id != 1:
        raise HTTPException(status_code=403, detail="No autorizado")
    return current_user

def get_current_medico_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.rol_id != 2:
        raise HTTPException(status_code=403, detail="No autorizado")
    return current_user

def get_current_enfermero_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.rol_id != 3:
        raise HTTPException(status_code=403, detail="No autorizado")
    return current_user
