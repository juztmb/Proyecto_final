from ..repository import JugadorRepository
from ..models import jugador_factory

class JugadorControlador:
    def __init__(self):
        self.repository = JugadorRepository()


    async def crear(self, body:dict):
        try:
            print(body)
            jugador = jugador_factory(body)
            print(jugador)
            return await self.repository.crear(jugador.to_dict())
        except Exception as e:
            print("error", e)
        
    async def obtener_por_id(self, id_jugador: str):
        try:
            print(id_jugador)
            jugador = await self.repository.obtener_por_id(id_jugador)
            print(jugador)
            if jugador == {}:
                return jugador
            else:
                return jugador_factory(jugador)
        except Exception as e:
            print(e)
    
    async def obtener_todos(self):
        try:
            return await self.repository.obtener_todos()
        except Exception as e:
            print(e)
    
    async def actualizar(self, body:dict):
        try:
            id_jugador = body["_id"]
            del body["_id"]
            return await self.repository.actualizar(id_jugador,body)
        except Exception as e:
            print(e)
    
    async def eliminar(self, id_jugador: str):
        try:
            return await self.repository.eliminar(id_jugador)
        except Exception as e:
            print(e)

