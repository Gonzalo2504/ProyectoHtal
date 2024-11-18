from sqlalchemy.orm import Session
from app.models import models
from app.schemas.administrador_schemas import AdministradorCreate, AdministradorUpdate
from app.auth import get_password_hash

#Crud crear administrador
def create_administrador(db: Session, administrador: AdministradorCreate):
    # Hash de la contraseña
    hashed_password = get_password_hash(administrador.contrasena)
    
    # Crear el objeto Administrador
    db_administrador = models.Administrador(
        nombre=administrador.nombre,
        apellido=administrador.apellido,
        dni=administrador.dni,
        email=administrador.email,
        telefono=administrador.telefono,
        usuario=administrador.usuario,
        contrasena=hashed_password,
        rol_id=1
        )
    
    # Agregar el nuevo administrador a la base de datos
    db.add(db_administrador)
    db.commit()
    db.refresh(db_administrador)
    return db_administrador

# Obtener la lista de administradores
def get_administradores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Administrador).offset(skip).limit(limit).all()

# Obtener un administrador por ID
def get_administrador(db: Session, administrador_id: int):
    return db.query(models.Administrador).filter(models.Administrador.id == administrador_id).first()

# Actualiza los datos de un administrador trae por id
# Recibe el id del administrador y un objeto con los datos a actualizar
def update_administrador(db: Session, administrador_id: int, administrador: AdministradorUpdate):
    # Busca el administrador en la base de datos
    db_administrador = db.query(models.Administrador).filter(models.Administrador.id == administrador_id).first()
    # Si el administrador existe
    if db_administrador:
        # Itera sobre los datos a actualizar
        for key, value in administrador.model_dump(exclude_unset=True).items():
            # Asigna el valor nuevo al atributo correspondiente del administrador
            setattr(db_administrador, key, value)
        # Guarda los cambios en la base de datos
        db.commit()
        # Refresca el objeto administrador
        db.refresh(db_administrador)
    # Retorna el administrador actualizado
    return db_administrador

# Eliminar un administrador por ID
def delete_administrador(db: Session, administrador_id: int):
    db_administrador = db.query(models.Administrador).filter(models.Administrador.id == administrador_id).first()
    if db_administrador:
        db.delete(db_administrador)
        db.commit()
    return db_administrador

