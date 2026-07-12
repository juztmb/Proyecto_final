from fastapi import APIRouter, HTTPException, Request
from ..controllers import PartidoControlador

"""Rutas HTTP para la gestión de partidos.

Expone los endpoints REST (crear, listar, obtener por id, actualizar y
eliminar) delegando toda la lógica de negocio en `PartidoControlador`,
incluyendo el procesamiento de estadísticas y cálculo de rendimiento de
jugadores cuando un partido finaliza.
"""

router_partido = APIRouter(prefix="/partido", tags=["Partidos"])
"""APIRouter: Enrutador de FastAPI con el prefijo "/partido" para todos los endpoints de partidos."""

# Instanciamos el controlador
controller = PartidoControlador()


@router_partido.post("/create")
async def crear(request: Request):
    """Registra un nuevo partido y procesa sus estadísticas.

    Si el partido recibido tiene estado "finished", el controlador calcula
    y persiste el rendimiento de cada jugador que participó, y actualiza
    los puntos de los equipos fantasy correspondientes.

    Args:
        request (Request): Petición HTTP cuyo cuerpo JSON contiene la
            información completa del partido (equipos, marcador, goles,
            tarjetas, sustituciones, alineaciones y estadísticas).

    Returns:
        dict: El resultado devuelto por el controlador (id del partido creado).

    Raises:
        HTTPException: Error 400 si ocurre un problema al procesar la petición.
    """
    try:
        body = await request.json()
        return await controller.crear(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_partido.get("/")
async def obtener_partidos():
    """Obtiene la lista completa de partidos registrados.

    Returns:
        list[dict]: Lista de partidos.
    """
    return await controller.obtener_todos()


@router_partido.get("/{partido_id}")
async def obtener_partidos_id(partido_id: str):
    """Obtiene un partido específico por su identificador.

    Args:
        partido_id (str): Identificador del partido (parámetro de ruta).

    Returns:
        dict: Información del partido encontrado.

    Raises:
        HTTPException: Error 404 si el partido no existe.
    """
    try:
        return await controller.obtener_por_id(partido_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_partido.put("/actualizar")
async def actualizar_partido(request: Request):
    """Actualiza la información de un partido existente.

    Args:
        request (Request): Petición HTTP cuyo cuerpo JSON debe incluir el
            "_id" del partido y los campos a actualizar.

    Returns:
        int: Cantidad de documentos modificados.

    Raises:
        HTTPException: Error 404 si el partido no existe.
    """
    try:
        body = await request.json()
        return await controller.actualizar(body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_partido.delete("/del/{partido_id}")
async def eliminar_partido(partido_id: str):
    """Elimina un partido de la base de datos.

    Args:
        partido_id (str): Identificador del partido a eliminar (parámetro de ruta).

    Returns:
        int: Cantidad de documentos eliminados.

    Raises:
        HTTPException: Error 404 si el partido no existe.
    """
    try:
        print(partido_id)
        return await controller.eliminar(partido_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
