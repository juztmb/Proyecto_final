from bson import ObjectId
from ..config import conexion


class PartidoRepository:
    def __init__(self):
        self.collection = conexion.get_db()["partidos"]

    async def crear(self, partido: dict):
        result = await self.collection.insert_one(partido)
        return str(result.inserted_id)

    async def obtener_por_id(self, partido_id: str):
        partido = await self.collection.find_one({"_id": partido_id})
        return partido
    
    async def obtener_todos(self):
        cursor = self.collection.find({})
        return [doc async for doc in cursor]

    async def actualizar(self, partido_id: str, datos: dict):
        result = await self.collection.update_one(
            {"_id": partido_id},
            {"$set": datos}
        )
        return result.modified_count

    async def eliminar(self, partido_id: str):
        result = await self.collection.delete_one({"_id": partido_id})
        return result.deleted_count