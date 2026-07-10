from bson import ObjectId
from ..config import conexion


class JugadorRepository:
    def __init__(self):
        self.collection = conexion.get_db()["jugadores"]

    async def crear(self, jugador: dict):
        result = await self.collection.insert_one(jugador)
        return str(result.inserted_id)

    async def obtener_por_id(self, jugador_id: str):
        jugador = await self.collection.find_one({"_id": jugador_id})
        return jugador
    
    async def obtener_por_nombre(self, nombre_jugador :str):
        jugador = await self.collection.find_one({'nombre': nombre_jugador})
        return jugador
    
    async def obtener_todos(self):
        cursor = self.collection.find({})
        return [doc async for doc in cursor]
    
    async def actualizar(self, jugador_id: str, datos: dict):
        result = await self.collection.update_one(
            {"_id": jugador_id},
            {"$set": datos}
        )
        return result.modified_count

    async def eliminar(self, jugador_id: str):
        result = await self.collection.delete_one({"_id": jugador_id})
        return result.deleted_count