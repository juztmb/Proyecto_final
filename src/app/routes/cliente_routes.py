from fastapi import APIRouter, HTTPException, Request
from ..controllers import UsuarioControlador

"""Rutas HTTP para la gestión de clientes y sus equipos fantasy.

Expone los endpoints REST para el registro de clientes, la creación de
equipos fantasy y el fichaje de jugadores (mercado de fichajes), delegando
toda la lógica de negocio en `UsuarioControlador`.
"""

router_cliente = APIRouter(prefix="/cliente", tags=["Usuarios"])
"""APIRouter: Enrutador de FastAPI con el prefijo "/cliente" para todos los endpoints de clientes."""

# Instanciamos el controlador
controller = UsuarioControlador()

@router_cliente.post("/login")
async def loguear(request: Request):
    try:
        body = await request.json()
        return await controller.obtener_por_correo(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router_cliente.get("/verificarE/{correo_info}")
async def verificar(correo_info: str):
    try:
        
        return await controller.verificar_email(correo_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_cliente.get('/equiposByIdUsuario/{usuario_id}')
async def obtener_equipos(usuario_id: str):
    try:
        return await controller.obtener_equipos(usuario_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router_cliente.post("/create")
async def crear(request: Request):
    """Crea un nuevo usuario cliente.

    Args:
        request (Request): Petición HTTP cuyo cuerpo JSON contiene los datos
            del cliente a crear (nombre, correo, contraseña, nombre de usuario, etc.).

    Returns:
        dict: El resultado devuelto por el controlador (id del cliente creado).

    Raises:
        HTTPException: Error 400 si ocurre un problema al procesar la petición.
    """
    try:
        body = await request.json()
        return await controller.crear(body)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_cliente.post("/crear_equipo")
async def crear_equipo(request: Request):
    """Crea un nuevo equipo fantasy para un cliente.

    Args:
        request (Request): Petición HTTP cuyo cuerpo JSON debe incluir
            "id_usuario" y "nombre_equipo".

    Returns:
        dict: El resultado devuelto por el controlador (id del equipo creado).

    Raises:
        HTTPException: Error 400 si ocurre un problema al procesar la petición.
    """
    try:
        body = await request.json()
        return await controller.crear_equipo(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router_cliente.delete("/deleteEquipo")
async def eliminar_equipo(request :Request):
    try:
        body = await request.json()
        return await controller.eliminar_equipobyID(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router_cliente.post('/agregar_jugador')
async def agregar_jugador_a_equipo(request: Request):
    """Ficha un jugador para un equipo fantasy (mercado de fichajes).

    Args:
        request (Request): Petición HTTP cuyo cuerpo JSON debe incluir
            "equipo_id" y "jugador_id".

    Returns:
        dict: El resultado devuelto por el controlador (cantidad de
        documentos modificados), o None si el jugador ya estaba en el equipo.

    Raises:
        HTTPException: Error 400 si ocurre un problema al procesar la petición.
    """
    try:
        body = await request.json()
        return await controller.agregar_jugador_equipo(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router_cliente.get('/obtenerJugador/{nombre_id}')
async def obtener_jugador_x_nombreReg(nombre_id : str ):
    try:
        return await controller.obtener_jugadorPorRegex(nombre_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router_cliente.put("/actualizar")
async def actualizar_usuario(request: Request):
    """Actualiza la información de un cliente existente.

    Args:
        request (Request): Petición HTTP cuyo cuerpo JSON debe incluir el
            "_id" del usuario y los campos a actualizar.

    Returns:
        int: Cantidad de documentos modificados.

    Raises:
        HTTPException: Error 404 si el usuario no existe.
    """
    try:
        body = await request.json()
        return await controller.actualizar(body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_cliente.delete("/del/{usuario_id}")
async def eliminar_cuenta(usuario_id: str):
    """Elimina la cuenta de un cliente de la base de datos.

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