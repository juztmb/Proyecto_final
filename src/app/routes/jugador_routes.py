from fastapi import APIRouter, HTTPException, Request
from ..controllers import JugadorControlador


router = APIRouter(prefix="/jugador", tags=["Jugadores"])

# Instanciamos el controlador
controller = JugadorControlador()


@router.post("/create")
async def crear(request: Request):
    try:
        body = await request.json()
        return await controller.crear(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def obtener_jugadores():
    return await controller.obtener_todos()


@router.get("/{jugador_id}")
async def obtener_jugador_id(jugador_id: str):
    try:
        return await controller.obtener_por_id(jugador_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/actualizar")
async def actualizar_jugador(request: Request):
    try:
        body = await request.json()
        return await controller.actualizar(body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/del/{jugador_id}")
async def eliminar_jugador(jugador_id: str):
    try:
        print(jugador_id)
        return await controller.eliminar(jugador_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))