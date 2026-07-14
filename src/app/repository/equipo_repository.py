from bson import ObjectId
from ..config import conexion


class EquipoRepository:
    """Repositorio encargado del acceso a datos de los equipos fantasy en MongoDB.

    Encapsula las operaciones CRUD sobre la colección "equipos_fantasy",
    desacoplando a los controladores del detalle de la base de datos
    (patrón Repository).

    Attributes:
        collection: Colección de MongoDB "equipos_fantasy".
    """
    def __init__(self):
        """Obtiene la conexión Singleton a la base de datos y la colección de equipos fantasy."""
        self.collection = conexion.get_db()["equipos_fantasy"]

    async def crear(self, equipo: dict):
        """Inserta un nuevo equipo fantasy en la base de datos.

        Args:
            equipo (dict): Datos del equipo a insertar.

        Returns:
            str: Identificador del documento insertado.
        """
        result = await self.collection.insert_one(equipo)
        return str(result.inserted_id)

    async def obtener_por_id(self, equipo_id: str):
        """Busca un equipo fantasy por su identificador.

        Args:
            equipo_id (str): Identificador del equipo.

        Returns:
            dict | None: Documento del equipo encontrado, o None si no existe.
        """
        equipo = await self.collection.find_one({"_id": ObjectId(equipo_id)})
        return equipo
    
    async def obtener_todos(self):
        """Obtiene todos los equipos fantasy registrados.

        Returns:
            list[dict]: Lista de documentos de equipos fantasy.
        """
        cursor = self.collection.find({})
        return [doc async for doc in cursor]
    
    async def actualizar(self, equipo_id: str, datos: dict):
        """Actualiza los datos de un equipo fantasy existente.

        Args:
            equipo_id (str): Identificador del equipo a actualizar.
            datos (dict): Campos a actualizar.

        Returns:
            int: Cantidad de documentos modificados.
        """
        result = await self.collection.update_one(
            {"_id": ObjectId(equipo_id)},
            {"$set": datos}
        )
        return result.modified_count
    
    async def obtener_x_usuario_id(self, usuario_id):
        lista_equipos = await self.collection.find({'id_usuario': usuario_id}).to_list(length=None)
        return lista_equipos
    
    async def actualizar_varios_equipos(self, jugador_id, puntos):
        """Suma puntos a todos los equipos fantasy que tengan a un jugador.

        Actualiza tanto el puntaje individual del jugador dentro de cada
        equipo como el puntaje total del equipo, en una sola operación
        masiva sobre todos los equipos que lo tengan fichado.

        Args:
            jugador_id (str): Identificador del jugador que sumó puntos.
            puntos (int | float): Puntos a sumar.

        Returns:
            UpdateResult: Resultado de la operación de actualización masiva
            (incluye cantidad de documentos encontrados y modificados).
        """
        
        result = await self.collection.update_many(
        { "jugadores_en_equipo.id": str(jugador_id)},
        { "$inc": { 
            f"jugadores_en_equipo.$.puntos": puntos,
            "puntos": puntos
            }})
        print("Resultado  =", result)
        return result
    
    async def agregar_jugador(self, equipo_id: str, jugador_info: dict):
        print(equipo_id)
        print(jugador_info)
        result = await self.collection.update_one(
            {"_id": ObjectId(equipo_id)},
            {
                    "$addToSet": {
                        "jugadores_en_equipo": {'id': jugador_info.get('id'), 'precio': jugador_info.get('precio'), 'posicion':jugador_info.get('posicion'), 'nombre': jugador_info.get('nombre'), 'puntos': jugador_info.get('puntos')}
                    }
            }
        )
        return {"modified": result.modified_count}
    
    async def eliminar_jugador_equipo(self, equipo_id, jugador_id):
        result = await self.collection.update_one(
            {'_id': ObjectId(equipo_id)},
            {
                "$pull": {
                    "jugadores_en_equipo": {
                        "id": str(jugador_id)
                            }
                    }
            }
        )
        return {
            "success": result.modified_count > 0
        }
    
    async def eliminar(self, equipo_id: str):
        """Elimina un equipo fantasy de la base de datos.

        Args:
            equipo_id (str): Identificador del equipo a eliminar.

        Returns:
            int: Cantidad de documentos eliminados.
        """
        result = await self.collection.delete_one({"_id": ObjectId(equipo_id)})
        return result.deleted_count