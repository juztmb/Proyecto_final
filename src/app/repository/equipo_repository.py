from bson import ObjectId
from ..config import conexion


class EquipoRepository:
    def __init__(self):
        self.collection = conexion.get_db()["equipos_fantasy"]

    async def crear(self, equipo: dict):
        result = await self.collection.insert_one(equipo)
        return str(result.inserted_id)

    async def obtener_por_id(self, equipo_id: str):
        equipo = await self.collection.find_one({"_id": ObjectId(equipo_id)})
        return equipo
    
    async def obtener_todos(self):
        cursor = self.collection.find({})
        return [doc async for doc in cursor]
    
    async def actualizar(self, equipo_id: str, datos: dict):
        result = await self.collection.update_one(
            {"_id": ObjectId(equipo_id)},
            {"$set": datos}
        )
        return result.modified_count
    
    async def actualizar_varios_equipos(self, jugador_id, puntos):
        result = await self.collection.update_many(
        { f"jugadores_en_equipo.{jugador_id}": {"$exists": True}},
        { "$inc": { 
            f"jugadores_en_equipo.{jugador_id}.puntos": puntos,
            "puntos": puntos
            }})
        return result

    async def eliminar(self, equipo_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(equipo_id)})
        return result.deleted_count