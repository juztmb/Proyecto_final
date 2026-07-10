from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    async def actualizar(self, datos_partido: dict):
        pass