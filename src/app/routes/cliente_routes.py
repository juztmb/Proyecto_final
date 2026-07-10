from fastapi import APIRouter, HTTPException, Request
from ..controllers import UsuarioControlador


router_cliente = APIRouter(prefix="/cliente", tags=["Usuarios"])

# Instanciamos el controlador
controller = UsuarioControlador()


@router_cliente.post("/create")
async def crear(request: Request):
    try:
        body = await request.json()
        return await controller.crear(body)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_cliente.post("/crear_equipo")
async def crear_equipo(request: Request):
    try:
        body = await request.json()
        return await controller.crear_equipo(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
router_cliente.post('/agregar_jugador')
async def agregar_jugador_a_equipo(request: Request):
    try:
        body = await request.json()
        return await controller.agregar_jugador_equipo(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router_cliente.put("/actualizar")
async def actualizar_usuario(request: Request):
    try:
        body = await request.json()
        return await controller.actualizar(body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_cliente.delete("/del/{usuario_id}")
async def eliminar_cuenta(usuario_id: str):
    try:
        print(usuario_id)
        return await controller.eliminar(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))