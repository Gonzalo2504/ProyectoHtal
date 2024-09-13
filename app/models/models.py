from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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
    estado = Column(String(255))
    estado_atencion = Column(String(50), default="en espera") #puede ser "en espera", "en triage" o "atendido"
    triage_id = Column(Integer, ForeignKey("triage_paciente.id_triage"))

    # Relación con TriagePaciente
    triages = relationship("TriagePaciente", back_populates="paciente")
    triage_actual = relationship("TriagePaciente")

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
    # Relación con TriagePaciente
    triages = relationship("TriagePaciente", back_populates="enfermero")

class TriagePaciente(Base):
    __tablename__ = "triage_paciente"

    id_triage = Column(Integer, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"))
    id_enfermmero = Column(Integer, ForeignKey("enfermeros.id"))
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

    # Relaciones con Paciente y Enfermero
    paciente = relationship("Paciente", back_populates="triages")
    enfermero = relationship("Enfermero", back_populates="triages")

