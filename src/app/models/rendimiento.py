from .estadisticas_strategy import EstadisticasStrategy


class Rendimiento():
    def __init__(self, jugador_id, partido_id, estadisticas_strategy: EstadisticasStrategy):
        self.__jugador_id = jugador_id
        self.__partido_id = partido_id
        self.__strategy = estadisticas_strategy
        self.__puntos = 0

    def calcular_puntos(self):
        self.__puntos = self.__strategy.calcular_puntos()

    def obtener_puntos(self):
        return self.__puntos
    
    def to_dict(self):
        return {
            'jugador_id':self.__jugador_id,
            'partido_id':self.__partido_id,
            'estadisticas':self.__strategy.obtener_estadisticas(),
            'puntos': self.__puntos

        }
