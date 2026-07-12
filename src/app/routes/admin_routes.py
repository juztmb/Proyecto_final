from fastapi import APIRouter, HTTPException, Request
from ..controllers import UsuarioControlador

"""Rutas HTTP para la gestión de administradores.

Expone los endpoints REST (crear, listar, obtener por id y eliminar)
delegando la lógica de negocio en `UsuarioControlador`. El endpoint de
creación exige un token especial de administrador para autorizar la
operación.
"""

router_administrador = APIRouter(prefix="/admin", tags=["Usuarios"])
"""APIRouter: Enrutador de FastAPI con el prefijo "/admin" para todos los endpoints de administradores."""

# Instanciamos el controlador
controller = UsuarioControlador()


@router_administrador.post("/create")
async def crear(request: Request):
    """Crea un nuevo usuario administrador.

    Solo procesa la creación si el cuerpo de la petición incluye el token
    de administrador válido; en caso contrario, rechaza la operación sin
    crear el usuario.

    Args:
        request (Request): Petición HTTP cuyo cuerpo JSON debe incluir los
            datos del administrador y el campo "token" con el token válido.

    Returns:
        dict: El resultado devuelto por el controlador (id del administrador
        creado), o un diccionario vacío si el token no es válido.

    Raises:
        HTTPException: Error 400 si ocurre un problema al procesar la petición.
    """
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
    """Obtiene la lista completa de usuarios registrados.

    Returns:
        list[dict]: Lista de usuarios.
    """
    return await controller.obtener_todos()


@router_administrador.get("/{usuario_id}")
async def obtener_usuario_id(usuario_id: str):
    """Obtiene un usuario específico por su identificador.

    Args:
        usuario_id (str): Identificador del usuario (parámetro de ruta).

    Returns:
        dict: Información del usuario encontrado.

    Raises:
        HTTPException: Error 404 si el usuario no existe.
    """
    try:
        return await controller.obtener_por_id(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_administrador.delete("/del/{usuario_id}")
async def eliminar_jugador(usuario_id: str):
    """Elimina un usuario de la base de datos.

    Args:
        usuario_id (str): Identificador del usuario a eliminar (parámetro de ruta).

    Returns:
        int: Cantidad de documentos eliminados.

    Raises:
        HTTPException: Error 404 si el usuario no existe.
    """
    try:
        print(usuario_id)
        return await controller.eliminar(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))