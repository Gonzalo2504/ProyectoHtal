from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import paciente_routes, medico_routes, enfermero_routes, administrador_routes, login_routes, triage_routes, ordenesMedicas_routes, evoluciones_routes, eventos_routes, informe_routes

app = FastAPI()

# Configuración del middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

#Rutas
app.include_router(paciente_routes.router, prefix="/api")
app.include_router(medico_routes.router, prefix="/api")
app.include_router(enfermero_routes.router, prefix="/api")
app.include_router(administrador_routes.router, prefix="/api")
app.include_router(login_routes.router, prefix="/api")
app.include_router(triage_routes.router, prefix="/api")
app.include_router(ordenesMedicas_routes.router, prefix="/api")
app.include_router(evoluciones_routes.router, prefix="/api")
app.include_router(eventos_routes.router, prefix="/api")
app.include_router(informe_routes.router, prefix="/api")