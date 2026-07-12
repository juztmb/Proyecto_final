from ..models import Observer
from ..repository import EquipoRepository
class PuntosEquipoControlador(Observer):
    """Observador concreto que actualiza los puntos de los equipos fantasy.

    Se suscribe a `PartidoControladorNotifier` y, cada vez que un jugador
    obtiene puntos en un partido, actualiza el puntaje de todos los equipos
    fantasy que lo tengan en su plantilla.

    Attributes:
        equipo_repository (EquipoRepository): Repositorio de equipos fantasy.
    """
    def __init__(self, equipo_repository : EquipoRepository):
        """Inicializa el observador con el repositorio de equipos a actualizar.

        Args:
            equipo_repository (EquipoRepository): Repositorio usado para
                propagar los puntos a los equipos fantasy correspondientes.
        """
        self.equipo_repository = equipo_repository

    async def actualizar(self, jugador_info: dict):
        """Reacciona a la notificación de un partido actualizando los equipos.

        Implementación del método `actualizar` definido por la interfaz
        `Observer`. Suma los puntos obtenidos por el jugador a todos los
        equipos fantasy en los que participa.

        Args:
            jugador_info (dict): Información del jugador notificada,
                debe incluir "_id" y "puntos".
        """
        jugador_id = jugador_info.get('_id')
        puntos = jugador_info['puntos']
        print(jugador_id)
        print(puntos)

        await self.equipo_repository.actualizar_varios_equipos(jugador_id=jugador_id, puntos=puntos)