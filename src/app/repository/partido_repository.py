from bson import ObjectId
from ..config import conexion


class PartidoRepository:
    """Repositorio encargado del acceso a datos de los partidos en MongoDB.

    Encapsula las operaciones CRUD sobre la colección "partidos",
    desacoplando a los controladores del detalle de la base de datos
    (patrón Repository).

    Attributes:
        collection: Colección de MongoDB "partidos".
    """
    def __init__(self):
        """Obtiene la conexión Singleton a la base de datos y la colección de partidos."""
        self.collection = conexion.get_db()["partidos"]

    async def crear(self, partido: dict):
        """Inserta un nuevo partido en la base de datos.

        Args:
            partido (dict): Datos del partido a insertar.

        Returns:
            str: Identificador del documento insertado.
        """
        result = await self.collection.insert_one(partido)
        return str(result.inserted_id)

    async def obtener_por_id(self, partido_id: str):
        """Busca un partido por su identificador.

        Args:
            partido_id (str): Identificador del partido.

        Returns:
            dict | None: Documento del partido encontrado, o None si no existe.
        """
        partido = await self.collection.find_one({"_id": partido_id})
        return partido
    
    async def obtener_todos(self):
        """Obtiene todos los partidos registrados.

        Returns:
            list[dict]: Lista de documentos de partidos.
        """
        cursor = self.collection.find({})
        return [doc async for doc in cursor]

    async def actualizar(self, partido_id: str, datos: dict):
        """Actualiza los datos de un partido existente.

        Args:
            partido_id (str): Identificador del partido a actualizar.
            datos (dict): Campos a actualizar.

        Returns:
            int: Cantidad de documentos modificados.
        """
        result = await self.collection.update_one(
            {"_id": partido_id},
            {"$set": datos}
        )
        return result.modified_count

    async def eliminar(self, partido_id: str):
        """Elimina un partido de la base de datos.

        Args:
            partido_id (str): Identificador del partido a eliminar.

        Returns:
            int: Cantidad de documentos eliminados.
        """
        result = await self.collection.delete_one({"_id": partido_id})
        return result.deleted_count