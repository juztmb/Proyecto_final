from ..models import Observer

class PuntosJugadorControlador(Observer):

    def __init__(self, jugador_repository):
        self.jugador_repository = jugador_repository
        

    async def actualizar(self, jugador_info: dict):
        jugador_id = jugador_info["_id"]
        del jugador_info["_id"] 
        await self.jugador_repository.actualizar(jugador_id, jugador_info)