from ..models import Observer

class PuntosJugadorControlador(Observer):
    """Observador concreto que actualiza las estadísticas de un jugador.

    Se suscribe a `PartidoControladorNotifier` y persiste en la base de
    datos las estadísticas actualizadas del jugador tras un partido.

    Attributes:
        jugador_repository (JugadorRepository): Repositorio de jugadores.
    """
    def __init__(self, jugador_repository):
        """Inicializa el observador con el repositorio de jugadores a actualizar.

        Args:
            jugador_repository (JugadorRepository): Repositorio usado para
                persistir los cambios de estadísticas del jugador.
        """
        self.jugador_repository = jugador_repository
        

    async def actualizar(self, jugador_info: dict):
        """Reacciona a la notificación de un partido actualizando al jugador.

        Implementación del método `actualizar` definido por la interfaz
        `Observer`.

        Args:
            jugador_info (dict): Datos del jugador a actualizar, debe incluir
                la clave "_id" con su identificador.
        """
        jugador_id = jugador_info["_id"]
        del jugador_info["_id"] 
        await self.jugador_repository.actualizar(jugador_id, jugador_info)