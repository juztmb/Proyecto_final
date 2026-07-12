from bson import ObjectId
from ..config import conexion


class RendimientoRepository:
    """Repositorio encargado del acceso a datos de los rendimientos en MongoDB.

    Un rendimiento representa las estadísticas y puntos obtenidos por un
    jugador en un partido específico. Encapsula las operaciones CRUD sobre
    la colección "rendimiento" (patrón Repository).

    Attributes:
        collection: Colección de MongoDB "rendimiento".
    """
    def __init__(self):
        """Obtiene la conexión Singleton a la base de datos y la colección de rendimientos."""
        self.collection = conexion.get_db()["rendimiento"]

    async def crear(self, rendimiento: dict):
        """Inserta un nuevo rendimiento en la base de datos.

        Args:
            rendimiento (dict): Datos del rendimiento a insertar (jugador,
                partido, estadísticas y puntos).

        Returns:
            str: Identificador del documento insertado.
        """
        result = await self.collection.insert_one(rendimiento)
        return str(result.inserted_id)

    async def obtener_por_id(self, rendimiento_id: str):
        """Busca un rendimiento por su identificador.

        Args:
            rendimiento_id (str): Identificador del rendimiento.

        Returns:
            dict | None: Documento del rendimiento encontrado, o None si no existe.
        """
        rendimiento = await self.collection.find_one({"_id": ObjectId(rendimiento_id)})
        return rendimiento
    
    async def obtener_todos_por_jugador_id(self, jugador_id :str):
        """Obtiene todos los rendimientos históricos de un jugador.

        Útil para calcular estadísticas individuales acumuladas del jugador
        a lo largo de la temporada.

        Args:
            jugador_id (str): Identificador del jugador.

        Returns:
            list[dict]: Lista de rendimientos asociados al jugador.
        """
        rendimientos = await self.collection.find({'jugador_id': jugador_id})
        return [doc async for doc in rendimientos]
    
    async def obtener_todos(self):
        """Obtiene todos los rendimientos registrados.

        Returns:
            list[dict]: Lista de documentos de rendimientos.
        """
        cursor = self.collection.find({})
        return [doc async for doc in cursor]
    
    async def actualizar(self, rendimiento_id: str, datos: dict):
        """Actualiza los datos de un rendimiento existente.

        Args:
            rendimiento_id (str): Identificador del rendimiento a actualizar.
            datos (dict): Campos a actualizar.

        Returns:
            int: Cantidad de documentos modificados.
        """
        result = await self.collection.update_one(
            {"_id": ObjectId(rendimiento_id)},
            {"$set": datos}
        )
        return result.modified_count

    async def eliminar(self, rendimiento_id: str):
        """Elimina un rendimiento de la base de datos.

        Args:
            rendimiento_id (str): Identificador del rendimiento a eliminar.

        Returns:
            int: Cantidad de documentos eliminados.
        """
        result = await self.collection.delete_one({"_id": ObjectId(rendimiento_id)})
        return result.deleted_count