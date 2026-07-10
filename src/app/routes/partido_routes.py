from fastapi import APIRouter, HTTPException, Request
from ..controllers import PartidoControlador


router_partido = APIRouter(prefix="/partido", tags=["Partidos"])

# Instanciamos el controlador
controller = PartidoControlador()


@router_partido.post("/create")
async def crear(request: Request):
    try:
        body = await request.json()
        return await controller.crear(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_partido.get("/")
async def obtener_partidos():
    return await controller.obtener_todos()


@router_partido.get("/{partido_id}")
async def obtener_partidos_id(partido_id: str):
    try:
        return await controller.obtener_por_id(partido_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_partido.put("/actualizar")
async def actualizar_partido(request: Request):
    try:
        body = await request.json()
        return await controller.actualizar(body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_partido.delete("/del/{partido_id}")
async def eliminar_jugador(partido_id: str):
    try:
        print(partido_id)
        return await controller.eliminar(partido_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
