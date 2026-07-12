from .estadisticas_strategy import EstadisticasStrategy


class Rendimiento():
    """Representa el rendimiento de un jugador en un partido específico.

    Utiliza el patrón Strategy (`EstadisticasStrategy`) para delegar el
    cálculo de puntos según la posición del jugador, sin conocer la lógica
    particular de cada una (Polimorfismo).

    Attributes:
        jugador_id (str): Identificador del jugador.
        partido_id (str): Identificador del partido.
        strategy (EstadisticasStrategy): Estrategia de cálculo de puntos
            correspondiente a la posición del jugador.
        puntos (float): Puntos obtenidos, calculados a partir de la estrategia.
    """
    def __init__(self, jugador_id, partido_id, estadisticas_strategy: EstadisticasStrategy):
        """Inicializa el rendimiento de un jugador en un partido.

        Args:
            jugador_id (str): Identificador del jugador.
            partido_id (str): Identificador del partido.
            estadisticas_strategy (EstadisticasStrategy): Estrategia de
                cálculo de puntos según la posición del jugador.
        """
        self.__jugador_id = jugador_id
        self.__partido_id = partido_id
        self.__strategy = estadisticas_strategy
        self.__puntos = 0

    def calcular_puntos(self):
        """Calcula y almacena los puntos del jugador delegando en la
        estrategia (`EstadisticasStrategy`) asignada.
        """
        self.__puntos = self.__strategy.calcular_puntos()

    def obtener_puntos(self):
        """Obtiene los puntos ya calculados para este rendimiento.

        Returns:
            float: Puntos obtenidos por el jugador en el partido.
        """
        return self.__puntos
    
    def to_dict(self):
        """Convierte el rendimiento a diccionario para persistirlo en la base de datos.

        Returns:
            dict: Representación del rendimiento (jugador, partido,
            estadísticas y puntos).
        """
        return {
            'jugador_id':self.__jugador_id,
            'partido_id':self.__partido_id,
            'estadisticas':self.__strategy.obtener_estadisticas(),
            'puntos': self.__puntos

        }
