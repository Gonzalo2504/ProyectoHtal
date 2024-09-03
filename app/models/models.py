from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
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
    
    # Relación con órdenes médicas
    ordenes_medicas = relationship("OrdenMedica", back_populates="paciente")
    # Relación con evoluciones por turno
    evoluciones_por_turno = relationship("EvolucionPorTurno", back_populates="paciente")

class OrdenMedica(Base):
    __tablename__ = "ordenes_medicas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    medico_id = Column(Integer, ForeignKey('medicos.id'))
    descripcion = Column(String(255))
    fecha_emision = Column(DateTime)
    estado = Column(String(255))

    paciente = relationship("Paciente", back_populates="ordenes_medicas")
    medico = relationship("Medico", back_populates="ordenes_medicas")

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
    ordenes_medicas = relationship("OrdenMedica", back_populates="medico")

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
    tareas_enfermeria = relationship("TareaEnfermeria", back_populates="enfermero")
    evoluciones_por_turno = relationship("EvolucionPorTurno", back_populates="enfermero")

class TareaEnfermeria(Base):
    __tablename__ = "tareas_enfermeria"

    id = Column(Integer, primary_key=True, index=True)
    orden_medica_id = Column(Integer, ForeignKey('ordenes_medicas.id'), nullable=True)
    enfermero_id = Column(Integer, ForeignKey('enfermeros.id'))
    tipo_tarea = Column(String(255))
    fecha_completada = Column(DateTime)
    notas = Column(String(255))

    orden_medica = relationship("OrdenMedica")
    enfermero = relationship("Enfermero", back_populates="tareas_enfermeria")

class EvolucionPorTurno(Base):
    __tablename__ = "evoluciones_por_turno"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    enfermero_id = Column(Integer, ForeignKey('enfermeros.id'))
    turno_inicio = Column(DateTime)
    turno_fin = Column(DateTime)
    resumen_tareas = Column(String(255))
    fecha_generacion = Column(DateTime)

    paciente = relationship("Paciente", back_populates="evoluciones_por_turno")
    enfermero = relationship("Enfermero", back_populates="evoluciones_por_turno")
