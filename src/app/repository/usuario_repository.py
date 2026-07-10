from bson import ObjectId
from ..config import conexion


class UsuarioRepository:
    def __init__(self):
        self.collection = conexion.get_db()["usuarios"]

    async def crear(self, usuario: dict):
        result = await self.collection.insert_one(usuario)
        return str(result.inserted_id)

    async def obtener_por_id(self, usuario_id: str):
        return await self.collection.find_one({"_id": ObjectId(usuario_id)})
    
    async def obtener_por_correo(self, correo: str):
        return await self.collection.find_one({"email": correo})
    
    async def obtener_todos(self):
        cursor = self.collection.find({})
        return [doc async for doc in cursor]

    async def actualizar(self, usuario_id: str, datos: dict):
        result = await self.collection.update_one(
            {"_id": ObjectId(usuario_id)},
            {"$set": datos}
        )
        return result.modified_count

    async def eliminar(self, usuario_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(usuario_id)})
        return result.deleted_count