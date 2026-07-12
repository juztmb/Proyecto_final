from fastapi import APIRouter, HTTPException, Request
from ..controllers import JugadorControlador

"""Rutas HTTP para la gestión de jugadores.

Expone los endpoints REST (crear, listar, obtener por id, actualizar y
eliminar) delegando toda la lógica de negocio en `JugadorControlador`.
"""

router = APIRouter(prefix="/jugador", tags=["Jugadores"])
"""APIRouter: Enrutador de FastAPI con el prefijo "/jugador" para todos los endpoints de jugadores."""

# Instanciamos el controlador
controller = JugadorControlador()


@router.post("/create")
async def crear(request: Request):
    """Crea un nuevo jugador.

    Args:
        request (Request): Petición HTTP cuyo cuerpo JSON contiene los datos
            del jugador a crear.

    Returns:
        dict: El resultado devuelto por el controlador (id del jugador creado).

    Raises:
        HTTPException: Error 400 si ocurre un problema al procesar la petición.
    """
    try:
        body = await request.json()
        return await controller.crear(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def obtener_jugadores():
    """Obtiene la lista completa de jugadores registrados.

    Returns:
        list[dict]: Lista de jugadores.
    """
    return await controller.obtener_todos()


@router.get("/{jugador_id}")
async def obtener_jugador_id(jugador_id: str):
    """Obtiene un jugador específico por su identificador.

    Args:
        jugador_id (str): Identificador del jugador (parámetro de ruta).

    Returns:
        dict: Información del jugador encontrado.

    Raises:
        HTTPException: Error 404 si el jugador no existe.
    """
    try:
        return await controller.obtener_por_id(jugador_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/actualizar")
async def actualizar_jugador(request: Request):
    """Actualiza la información de un jugador existente.

    Args:
        request (Request): Petición HTTP cuyo cuerpo JSON debe incluir el
            "_id" del jugador y los campos a actualizar.

    Returns:
        int: Cantidad de documentos modificados.

    Raises:
        HTTPException: Error 404 si el jugador no existe.
    """
    try:
        body = await request.json()
        return await controller.actualizar(body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/del/{jugador_id}")
async def eliminar_jugador(jugador_id: str):
    """Elimina un jugador de la base de datos.

    Args:
        jugador_id (str): Identificador del jugador a eliminar (parámetro de ruta).

    Returns:
        int: Cantidad de documentos eliminados.

    Raises:
        HTTPException: Error 404 si el jugador no existe.
    """
    try:
        print(jugador_id)
        return await controller.eliminar(jugador_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))