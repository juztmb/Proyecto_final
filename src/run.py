from fastapi import FastAPI
from app.routes.jugador_routes import router as jugador_routes
from app.routes import router_partido as partido_router
from app.routes import router_administrador as admin_router


app = FastAPI(title="API MVC con MongoDB (Sin Beanie)")

# Incluimos las rutas (Vistas)
app.include_router(jugador_routes)
app.include_router(partido_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente. Ve a /docs para probarla."}