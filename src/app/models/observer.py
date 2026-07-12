from abc import ABC, abstractmethod

class Observer(ABC):
    """Interfaz del patrón Observer.

    Debe ser implementada por toda clase que necesite reaccionar a eventos
    de partido (por ejemplo, actualizar puntos de jugadores o de equipos
    fantasy) sin acoplarse directamente a quien genera el evento
    (`PartidoNotifier`).
    """
    @abstractmethod
    async def actualizar(self, datos_partido: dict):
        """Reacciona a una notificación emitida por un `PartidoNotifier`.

        Args:
            datos_partido (dict): Información relevante del evento notificado
                (por ejemplo, estadísticas o puntos de un jugador).
        """
        pass