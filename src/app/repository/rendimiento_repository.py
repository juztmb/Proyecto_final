from bson import ObjectId
from ..config import conexion


class RendimientoRepository:
    def __init__(self):
        self.collection = conexion.get_db()["rendimiento"]

    async def crear(self, rendimiento: dict):
        result = await self.collection.insert_one(rendimiento)
        return str(result.inserted_id)

    async def obtener_por_id(self, rendimiento_id: str):
        rendimiento = await self.collection.find_one({"_id": ObjectId(rendimiento_id)})
        return rendimiento
    
    async def obtener_todos_por_jugador_id(self, jugador_id :str):
        rendimientos = await self.collection.find({'jugador_id': jugador_id})
        return [doc async for doc in rendimientos]
    
    async def obtener_todos(self):
        cursor = self.collection.find({})
        return [doc async for doc in cursor]
    
    async def actualizar(self, rendimiento_id: str, datos: dict):
        result = await self.collection.update_one(
            {"_id": ObjectId(rendimiento_id)},
            {"$set": datos}
        )
        return result.modified_count

    async def eliminar(self, rendimiento_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(rendimiento_id)})
        return result.deleted_count