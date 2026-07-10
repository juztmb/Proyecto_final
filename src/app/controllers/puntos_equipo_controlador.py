from ..models import Observer
from ..repository import EquipoRepository
class PuntosEquipoControlador(Observer):
    def __init__(self, equipo_repository : EquipoRepository):
        self.equipo_repository = equipo_repository

    async def actualizar(self, jugador_info: dict):
        jugador_id = jugador_info.get('_id')
        puntos = jugador_info['puntos']
        print(jugador_id)
        print(puntos)

        await self.equipo_repository.actualizar_varios_equipos(jugador_id=jugador_id, puntos=puntos)