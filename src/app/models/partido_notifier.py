from .observer import Observer


class PartidoNotifier:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    async def notify(self, partido_info: dict):
        for observer in self._observers:
            await observer.actualizar(partido_info)
    
    