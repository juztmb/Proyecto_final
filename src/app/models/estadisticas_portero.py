from .estadisticas_strategy import EstadisticasStrategy


class EstadisticasPortero(EstadisticasStrategy):
    """Estrategia de cálculo de puntos para la posición de Portero.

    Pondera especialmente las atajadas, los goles evitados (portería en
    cero) y penaliza fuertemente los goles en contra.

    Attributes:
        atajadas (int): Cantidad de atajadas realizadas en el partido.
        goles (int): Goles anotados por el portero.
        asistencias (int): Asistencias realizadas.
        tarjetas_amarillas (int): Tarjetas amarillas recibidas.
        tarjetas_rojas (int): Tarjetas rojas recibidas.
        minutos_jugados (int): Minutos jugados en el partido.
        goles_en_contra (int): Goles recibidos por su equipo mientras jugaba.
    """
    def __init__(self, atajadas, goles, asistencias, tarjeta_amarilla, tarjeta_roja, minutos_juego, goles_en_contra):
        """Inicializa las estadísticas del portero para un partido.

        Args:
            atajadas (int): Cantidad de atajadas realizadas.
            goles (int): Goles anotados.
            asistencias (int): Asistencias realizadas.
            tarjeta_amarilla (int): Tarjetas amarillas recibidas.
            tarjeta_roja (int): Tarjetas rojas recibidas.
            minutos_juego (int): Minutos jugados.
            goles_en_contra (int): Goles recibidos mientras jugaba.
        """
        self.__atajadas = atajadas
        self.__goles = goles
        self.__asistencias = asistencias
        self.__tarjetas_amarillas = tarjeta_amarilla
        self.__tarjetas_rojas = tarjeta_roja
        self.__minutos_jugados = minutos_juego
        self.__goles_en_contra = goles_en_contra

    def calcular_puntos(self):
        """Calcula los puntos fantasy del portero.

        Reglas aplicadas: +1 punto cada 3 atajadas, +10 por gol, +3 por
        asistencia, -2 por tarjeta amarilla, -5 por tarjeta roja, +1 o +2
        por minutos jugados (≤60 / >60), +4 si termina con portería en cero
        habiendo jugado 60+ minutos, y -2 por cada 2 goles en contra.

        Returns:
            float: Puntos totales obtenidos por el portero en el partido.
        """
        puntos = 0
        puntos += (self.__atajadas//3) * 1
        puntos += (self.__goles) * 10
        puntos += (self.__asistencias) * 3
        puntos -= (self.__tarjetas_amarillas) * 2
        puntos -= (self.__tarjetas_rojas) *5
        if self.__minutos_jugados <= 60:
            puntos += 1
        elif self.__minutos_jugados >60:
            puntos += 2
        else:
            puntos +=0

        if self.__goles_en_contra == 0 and self.__minutos_jugados >=60:
            puntos += 4 
        
        puntos -= (self.__goles_en_contra//2) *2
        
        return puntos 

    def obtener_estadisticas(self):
        """Devuelve las estadísticas crudas del portero.

        Returns:
            dict: Estadísticas del portero (atajadas, goles, asistencias,
            tarjetas, minutos jugados y goles en contra).
        """
        return {
            "atajadas": self.__atajadas,
            "goles": self.__goles,
            "asistencias": self.__asistencias,
            "tarjetas_amarillas": self.__tarjetas_amarillas,
            "tarjetas_rojas": self.__tarjetas_rojas,
            "minutos_jugados": self.__minutos_jugados,
            "goles_en_contra": self.__goles_en_contra
        }

