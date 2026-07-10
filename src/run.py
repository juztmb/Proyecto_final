from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.routes.jugador_routes import router as jugador_routes
from app.routes import router_partido as partido_router
from app.routes import router_administrador as admin_router

app = FastAPI(title="API MVC con MongoDB (Sin Beanie)")

# Permisos CORS para conectar tu HTML y Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos las rutas de tus compañeros
app.include_router(jugador_routes)
app.include_router(partido_router)
app.include_router(admin_router)

# Como 'static' está en la misma carpeta que 'run.py', solo necesitamos un nivel
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")