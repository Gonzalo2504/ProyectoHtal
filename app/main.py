from fastapi import FastAPI
from app.routes import paciente_routes, medico_routes, enfermero_routes, administrador_routes, login_routes

app = FastAPI()

#Rutas
app.include_router(paciente_routes.router, prefix="/api")
app.include_router(medico_routes.router, prefix="/api")
app.include_router(enfermero_routes.router, prefix="/api")
app.include_router(administrador_routes.router, prefix="/api")
app.include_router(login_routes.router, prefix="/api")