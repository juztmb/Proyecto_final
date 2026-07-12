from ..models import PartidoNotifier


class PartidoControladorNotifier(PartidoNotifier):
    """Sujeto (Subject) concreto del patrón Observer para eventos de partido.

    Hereda de `PartidoNotifier` y expone un método específico para notificar
    a todos los observadores suscritos (por ejemplo, los controladores que
    actualizan puntos de jugadores y de equipos) cuando se calculan las
    estadísticas de un jugador en un partido.
    """
    def __init__(self):
        """Inicializa el notificador reutilizando la lista de observadores
        definida en la clase base `PartidoNotifier`.
        """
        super().__init__()

    async def notificar(self, estadisticas_partido: dict):
        """Notifica a todos los observadores suscritos con las estadísticas del partido.

        Args:
            estadisticas_partido (dict): Información del jugador/estadísticas
                a propagar a los observadores (Observer.actualizar).
        """
        await self.notify(estadisticas_partido)