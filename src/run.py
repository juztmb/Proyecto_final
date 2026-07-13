from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from app.routes.jugador_routes import router as jugador_routes
from app.routes import router_partido as partido_router
from app.routes import router_administrador as admin_router
<<<<<<< HEAD
from app.routes import router_cliente as cliente_router
=======
from app.routes import router_cliente
>>>>>>> bd612ad (revisando view, agregando pagina incial y pagina para crear cuenta y abrir cuenta)

app = FastAPI(title="API MVC Fantasy Football Mundial 2026 con MongoDB")

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
<<<<<<< HEAD
app.include_router(cliente_router)
=======
app.include_router(router_cliente)
>>>>>>> bd612ad (revisando view, agregando pagina incial y pagina para crear cuenta y abrir cuenta)

# Como 'static' está en la misma carpeta que 'run.py', solo necesitamos un nivel
base_dir = Path(__file__).resolve().parent
static_dir = base_dir / "static"

#app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

<<<<<<< HEAD
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
=======
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
>>>>>>> bd612ad (revisando view, agregando pagina incial y pagina para crear cuenta y abrir cuenta)
