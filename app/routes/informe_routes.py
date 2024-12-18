from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Paciente, TriagePaciente, EvolucionPaciente, OrdenMedica, Evento  
from datetime import datetime
from fpdf import FPDF
import os
from app.auth import get_user_by_role, Usuario

router = APIRouter()

def generar_informe_paciente(session: Session, paciente_id: int, nombre_archivo: str):
    # Obtener información del paciente
    paciente = session.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise ValueError("Paciente no encontrado")
    
    # Crear el PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Encabezado
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, f"Informe del Paciente: {paciente.nombre} {paciente.apellido}", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    # Información del paciente
    pdf.cell(0, 10, f"Paciente: {paciente.nombre} {paciente.apellido} (DNI: {paciente.dni})", ln=True)
    
    # Último Triage
    triage = session.query(TriagePaciente).filter(TriagePaciente.id_paciente == paciente_id).order_by(TriagePaciente.fecha_y_hora.desc()).first()
    if triage:
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, "Último Triage:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Fecha y hora: {triage.fecha_y_hora.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(0, 10, f"Clasificación: {triage.clasificacion}", ln=True)
        pdf.cell(0, 10, f"Motivo de consulta: {triage.motivo_consulta}", ln=True)
        pdf.cell(0, 10, f"Observaciones: {triage.observaciones}", ln=True)
        pdf.ln(10)
    
    # Última Orden Médica
    orden = session.query(OrdenMedica).filter(OrdenMedica.id_paciente == paciente_id).order_by(OrdenMedica.fecha_y_hora.desc()).first()
    if orden:
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, "Última Orden Médica:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Fecha y hora: {orden.fecha_y_hora.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(0, 10, f"Descripción: {orden.descripcion}", ln=True)
        pdf.cell(0, 10, f"Observaciones: {orden.observaciones if orden.observaciones else 'N/A'}", ln=True)
        pdf.ln(10)
    
    # Última Evolución
    evolucion = session.query(EvolucionPaciente).filter(EvolucionPaciente.id_paciente == paciente_id).order_by(EvolucionPaciente.fecha_y_hora.desc()).first()
    if evolucion:
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, "Última Evolución:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Fecha y hora: {evolucion.fecha_y_hora.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(0, 10, f"Descripción: {evolucion.descripcion}", ln=True)
        pdf.ln(10)
    
    # Último Evento
    evento = session.query(Evento).filter(Evento.paciente_id == paciente_id).order_by(Evento.fecha_hora.desc()).first()
    if evento:
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, "Último Evento:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Fecha y hora: {evento.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(0, 10, f"Tipo de evento: {evento.tipo_evento}", ln=True)
        pdf.cell(0, 10, f"Observaciones: {evento.observaciones if evento.observaciones else 'N/A'}", ln=True)
        pdf.ln(10)
    
    # Guardar el PDF
    pdf.output(nombre_archivo)

@router.get("/pacientes/{paciente_id}/realizar_informe")
def realizar_informe(paciente_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_user_by_role([1]))):
    # Nombre del archivo temporal
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo = f"informe_paciente_{paciente_id}_{timestamp}.pdf"
    
    # Generar el informe
    try:
        generar_informe_paciente(db, paciente_id, nombre_archivo)
    except Exception as e:
        return {"error": str(e)}
    
    # Retornar el archivo como respuesta
    return FileResponse(nombre_archivo, media_type='application/pdf', filename=nombre_archivo)

