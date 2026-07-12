from .observer import Observer


class PartidoNotifier:
    """Sujeto (Subject) base del patrón Observer para eventos de partido.

    Mantiene la lista de observadores suscritos y permite notificarles
    cambios (por ejemplo, cuando se calculan los puntos de un jugador tras
    un partido), desacoplando al emisor del evento de quienes reaccionan a él.

    Attributes:
        _observers (list[Observer]): Observadores suscritos a las notificaciones.
    """
    def __init__(self):
        """Inicializa el notificador con una lista vacía de observadores."""
        self._observers = []

    def attach(self, observer: Observer):
        """Suscribe un nuevo observador a las notificaciones.

        Args:
            observer (Observer): Observador que reaccionará a los eventos notificados.
        """
        self._observers.append(observer)

    async def notify(self, partido_info: dict):
        """Notifica a todos los observadores suscritos.

        Args:
            partido_info (dict): Información del evento a propagar a cada observador.
        """
        for observer in self._observers:
            await observer.actualizar(partido_info)
    
    