from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.jugador_routes import router as jugador_routes
from app.routes import router_partido as partido_router
from app.routes import router_administrador as admin_router

app = FastAPI(title="API MVC con MongoDB (Sin Beanie)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],



app.include_router(jugador_routes)
app.include_router(partido_router)
app.include_router(admin_router)


app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
