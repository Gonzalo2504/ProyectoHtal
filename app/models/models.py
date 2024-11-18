from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app.database import Base

Base = declarative_base()

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True)

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), index=True)
    apellido = Column(String(255), index=True)
    dni = Column(Integer, index=True, unique=True)
    email = Column(String(255))
    telefono = Column(String(255))
    usuario = Column(String(255))
    contrasena = Column(String(255))
    rol_id = Column(Integer, ForeignKey("roles.id"))

    rol = relationship("Rol")

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), index=True)
    apellido = Column(String(255), index=True)
    dni = Column(Integer, index=True)
    fecha_nacimiento = Column(DateTime)
    direccion = Column(String(255))
    telefono = Column(String(255))
    email = Column(String(255))
    estado_atencion = Column(String(50), default="en espera") #puede ser "en espera" o "atendido"


class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), index=True)
    apellido = Column(String(255), index=True)
    dni = Column(Integer, index=True, unique=True)
    especialidad = Column(String(255))
    email = Column(String(255))
    telefono = Column(String(255))
    usuario = Column(String(255))
    contrasena = Column(String(255))
    rol_id = Column(Integer, ForeignKey("roles.id"))    

    rol = relationship("Rol")

class Enfermero(Base):
    __tablename__ = "enfermeros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    apellido = Column(String(255), index=True)
    dni = Column(Integer, index=True, unique=True)
    email = Column(String(255))
    telefono = Column(String(255))
    usuario = Column(String(255))
    contrasena = Column(String(255))
    rol_id = Column(Integer, ForeignKey("roles.id"))
    
    rol = relationship("Rol")

class TriagePaciente(Base):
    __tablename__ = "triage_paciente"

    id_triage = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    id_enfermero = Column(Integer, ForeignKey("enfermeros.id"), nullable=False)
    fecha_y_hora = Column(DateTime, default=func.now())
    clasificacion = Column(String(255))
    antecedentes = Column(String(255))
    frecuencia_cardiaca = Column(String(255))
    presion_arterial_sistolica = Column(String(255))
    presion_arterial_diastolica = Column(String(255))
    temperatura = Column(String(255))
    frecuencia_respiratoria = Column(String(255))
    saturacion_oxigeno = Column(String(255))
    motivo_consulta = Column(String(255))
    observaciones = Column(String(255))
    
    paciente = relationship("Paciente")
    enfermero = relationship("Enfermero")

class OrdenMedica(Base):
    __tablename__ = 'ordenes_medicas'

    id = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    id_medico = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    fecha_y_hora = Column(DateTime, default=func.now())
    descripcion = Column(Text, nullable=False)
    observaciones = Column(Text)

    paciente = relationship("Paciente")
    medico = relationship("Medico")



