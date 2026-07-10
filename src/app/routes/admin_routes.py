from fastapi import APIRouter, HTTPException, Request
from ..controllers import UsuarioControlador


router_administrador = APIRouter(prefix="/admin", tags=["Usuarios"])

# Instanciamos el controlador
controller = UsuarioControlador()


@router_administrador.post("/create")
async def crear(request: Request):
    try:
        
        body = await request.json()
        if body.get('token') != None and body.get('token') == "QWRtaW5pc3RyYWRvckFwbGljYWNpb24":
            return await controller.crear(body)
        else:
            print('Solo un administrador puede crear este usuario')
            return {}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_administrador.get("/")
async def obtener_usuarios():
    return await controller.obtener_todos()


@router_administrador.get("/{usuario_id}")
async def obtener_usuario_id(usuario_id: str):
    try:
        return await controller.obtener_por_id(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_administrador.delete("/del/{usuario_id}")
async def eliminar_jugador(usuario_id: str):
    try:
        print(usuario_id)
        return await controller.eliminar(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))