from abc import ABC, abstractmethod


class EstadisticasStrategy(ABC):
    @abstractmethod
    def calcular_puntos(self):
        pass
    @abstractmethod
    def obtener_estadisticas(self):
        pass

    