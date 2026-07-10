from ..models import PartidoNotifier


class PartidoControladorNotifier(PartidoNotifier):
    def __init__(self):
        super().__init__()

    async def notificar(self, estadisticas_partido: dict):
        await self.notify(estadisticas_partido)