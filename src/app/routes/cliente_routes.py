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

    """
        Endpoint para verificar si un correo electrónico ya está registrado.

        Args:
            correo_info (str): Correo electrónico a verificar, recibido como
                parámetro de ruta.

        Returns:
            dict: Resultado devuelto por `controller.verificar_email`, con la forma:
                {'existe': True}  -> si el correo ya está registrado.
                {'existe': False} -> si el correo no está registrado.

        Raises:
            HTTPException: Con código 400 si ocurre algún error durante el proceso,
                incluyendo el detalle del error original en el mensaje.
    """
    try:
        
        return await controller.verificar_email(correo_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_cliente.get('/equiposByIdUsuario/{usuario_id}')
async def obtener_equipos(usuario_id: str):
    """
        Endpoint para obtener los equipos asociados a un usuario específico.

        Args:
            usuario_id (str): Identificador del usuario, recibido como parámetro
                de ruta.

        Returns:
            list[dict]: Lista de equipos del usuario devuelta por
                `controller.obtener_equipos`, donde cada equipo contiene:
                    - id (str): Identificador del equipo.
                    - name (str): Nombre del equipo.
                    - crest (str): Color representativo del equipo.
                    - players (list): Jugadores del equipo.
                    - points (int | float): Puntos acumulados por el equipo.

        Raises:
            HTTPException: Con código 400 si ocurre algún error durante el proceso,
                incluyendo el detalle del error original en el mensaje.
    """
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
    """
        Endpoint para eliminar un equipo a partir de su ID.

        Args:
            request (Request): Objeto de la petición HTTP, cuyo cuerpo (JSON)
                debe contener la información necesaria para identificar el
                equipo a eliminar (por ejemplo, el ID del equipo).

        Returns:
            El resultado devuelto por `controller.eliminar_equipobyID`, que
            típicamente confirma la eliminación del equipo.

    """
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

    """
    try:
        body = await request.json()
        return await controller.agregar_jugador_equipo(body)
    except Exception:
        raise
    except Exception as e:
        print('error', e)
        raise HTTPException(status_code=400, detail=str(e))
    
@router_cliente.delete('/deleteJugadorEquipo')
async def eliminar_jugador_equipo(request : Request):
    """
        Endpoint para eliminar un jugador de un equipo.

        Args:
            request (Request): Objeto de la petición HTTP, cuyo cuerpo (JSON)
                debe contener la información necesaria para identificar al
                jugador y al equipo del cual se desea eliminar (por ejemplo,
                el ID del equipo y el ID del jugador).

        Returns:
            El resultado devuelto por `controller.eliminar_jugador_equipo`, que
            típicamente confirma la eliminación del jugador dentro del equipo.
    """
    try:
        body = await request.json()
        return await controller.eliminar_jugador_equipo(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router_cliente.get('/obtenerJugador/{nombre_id}')
async def obtener_jugador_x_nombreReg(nombre_id : str ):
    """
        Endpoint para buscar jugadores cuyo nombre coincida parcialmente con
        el texto proporcionado, utilizando búsqueda por expresión regular.

    Args:
        nombre_id (str): Texto o patrón a buscar dentro del nombre del
            jugador, recibido como parámetro de ruta.

    Returns:
        list[dict]: Lista de jugadores encontrados, devuelta por
            `controller.obtener_jugadorPorRegex`, donde cada jugador contiene:
                - id (str): Identificador del jugador.
                - nombre (str): Nombre del jugador.
                - posicion (str): Posición del jugador.
                - precio (float | int): Precio del jugador.
                - equipo (str): Equipo al que pertenece el jugador.
    """
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