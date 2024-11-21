from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE
from app.models.models import Administrador, Medico, Enfermero
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from typing import List, Union

# Define el esquema para extraer el token de la cabecera "Authorization"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear una contraseña
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar una contraseña plana contra la hasheada
def verify_password(password_plano: str, hashed_password: str) -> bool:
    return pwd_context.verify(password_plano, hashed_password)

# Función para crear un token de acceso
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para obtener el usuario actual
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        id: int = payload.get("id_usuario")
        rol_id: int = payload.get("rol_id")
        if usuario is None or id is None or rol_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Buscar el usuario en la base de datos según su rol
    user = None
    if rol_id == 1:  # Administrador
        user = db.query(Administrador).filter(Administrador.usuario == usuario).first()
    elif rol_id == 2:  # Médico
        user = db.query(Medico).filter(Medico.usuario == usuario).first()
    elif rol_id == 3:  # Enfermero
        user = db.query(Enfermero).filter(Enfermero.usuario == usuario).first()

    if user is None:
        raise credentials_exception
    
    user.id_usuario = id

    return user

# Función para validar roles permitidos
def get_user_by_role(roles_permitidos: List[int]):
    def role_validator(current_user: Usuario = Depends(get_current_user)):
        if current_user.rol_id not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado"
            )
        return current_user
    return role_validator

# Alias para el tipo de usuario
Usuario = Union[Medico, Administrador, Enfermero]