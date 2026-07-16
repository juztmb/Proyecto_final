from bson import ObjectId
from ..config import conexion
import re


class JugadorRepository:
    """Repositorio encargado del acceso a datos de los jugadores en MongoDB.

    Encapsula las operaciones CRUD sobre la colección "jugadores",
    desacoplando a los controladores del detalle de la base de datos
    (patrón Repository).

    Attributes:
        collection: Colección de MongoDB "jugadores".
    """
    def __init__(self):
        """Obtiene la conexión Singleton a la base de datos y la colección de jugadores."""
        self.collection = conexion.get_db()["jugadores"]

    async def crear(self, jugador: dict):
        """Inserta un nuevo jugador en la base de datos.

        Args:
            jugador (dict): Datos del jugador a insertar.

        Returns:
            str: Identificador del documento insertado.
        """
        result = await self.collection.insert_one(jugador)
        return str(result.inserted_id)

    async def obtener_por_id(self, jugador_id: str):
        """Busca un jugador por su identificador.

        Args:
            jugador_id (str): Identificador del jugador.

        Returns:
            dict | None: Documento del jugador encontrado, o None si no existe.
        """
        jugador = await self.collection.find_one({"_id": jugador_id})
        return jugador
    
    async def obtener_por_nombre_regex(self, nombre_jugador: str):
        """
            Busca en la base de datos jugadores cuyo nombre coincida parcialmente
            (sin distinguir mayúsculas/minúsculas) con el texto proporcionado,
            limitando el resultado a un máximo de 10 documentos.

            Args:
                nombre_jugador (str): Texto o patrón a buscar dentro del campo
                    "nombre" de los jugadores. Se escapa automáticamente con
                    `re.escape` para evitar que caracteres especiales de regex
                    (como '.', '*', '(', etc.) sean interpretados como parte
                    de la expresión regular.

            Returns:
                list[dict]: Lista de hasta 10 documentos de jugadores (en formato
                    crudo de MongoDB) que coinciden con el nombre buscado. Retorna
                    una lista vacía si no se encuentra ningún jugador.
        """
        lista_jugadores = await self.collection.find({
            "nombre": {
                "$regex": re.escape(nombre_jugador),
                "$options": "i"
            }
        }).limit(10).to_list(length=10)
        return lista_jugadores
    async def obtener_por_nombre(self, nombre_jugador :str):
        """Busca un jugador por su nombre.

        Args:
            nombre_jugador (str): Nombre del jugador a buscar.

        Returns:
            dict | None: Documento del jugador encontrado, o None si no existe.
        """
        jugador = await self.collection.find_one({'nombre': nombre_jugador})
        return jugador
    
    async def obtener_todos(self):
        """Obtiene todos los jugadores registrados.

        Returns:
            list[dict]: Lista de documentos de jugadores.
        """
        cursor = self.collection.find({})
        return [doc async for doc in cursor]
    
    async def actualizar(self, jugador_id: str, datos: dict):
        """Actualiza los datos de un jugador existente.

        Args:
            jugador_id (str): Identificador del jugador a actualizar.
            datos (dict): Campos a actualizar.

        Returns:
            int: Cantidad de documentos modificados.
        """
        result = await self.collection.update_one(
            {"_id": jugador_id},
            {"$set": datos}
        )
        return result.modified_count

    async def eliminar(self, jugador_id: str):
        """Elimina un jugador de la base de datos.

        Args:
            jugador_id (str): Identificador del jugador a eliminar.

        Returns:
            int: Cantidad de documentos eliminados.
        """
        result = await self.collection.delete_one({"_id": jugador_id})
        return result.deleted_count