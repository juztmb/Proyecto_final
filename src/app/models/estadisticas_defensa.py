from .estadisticas_strategy import EstadisticasStrategy


class EstadisticasDefensa(EstadisticasStrategy):
    """Estrategia de cálculo de puntos para la posición de Defensa.

    Pondera la portería en cero del equipo y los pases completados, además
    de goles, asistencias y tarjetas.

    Attributes:
        goles (int): Goles anotados.
        asistencias (int): Asistencias realizadas.
        tarjetas_amarillas (int): Tarjetas amarillas recibidas.
        tarjetas_rojas (int): Tarjetas rojas recibidas.
        minutos_jugados (int): Minutos jugados en el partido.
        goles_en_contra (int): Goles recibidos por su equipo mientras jugaba.
        pases_completados (int): Pases completados durante el partido.
    """
    def __init__(self, goles, asistencias, tarjeta_amarilla, tarjeta_roja, minutos_juego, goles_en_contra, pases_completados):
        """Inicializa las estadísticas del defensa para un partido.

        Args:
            goles (int): Goles anotados.
            asistencias (int): Asistencias realizadas.
            tarjeta_amarilla (int): Tarjetas amarillas recibidas.
            tarjeta_roja (int): Tarjetas rojas recibidas.
            minutos_juego (int): Minutos jugados.
            goles_en_contra (int): Goles recibidos mientras jugaba.
            pases_completados (int): Pases completados en el partido.
        """
        self.__goles = goles
        self.__asistencias = asistencias
        self.__tarjetas_amarillas = tarjeta_amarilla
        self.__tarjetas_rojas = tarjeta_roja
        self.__minutos_jugados = minutos_juego
        self.__goles_en_contra = goles_en_contra
        self.__pases_completados = pases_completados

    def calcular_puntos(self):
        """Calcula los puntos fantasy del defensa.

        Reglas aplicadas: +6 por gol, +3 por asistencia, -2 por tarjeta
        amarilla, -5 por tarjeta roja, +1 o +2 por minutos jugados
        (≤60 / >60), +4 si termina con portería en cero habiendo jugado
        60+ minutos, -2 por cada 2 goles en contra, y +1 por cada 20 pases
        completados.

        Returns:
            float: Puntos totales obtenidos por el defensa en el partido.
        """
        puntos = 0
        puntos += (self.__goles) * 6
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
        puntos += (self.__pases_completados//20) * 1
        return puntos 

    def obtener_estadisticas(self):
        """Devuelve las estadísticas crudas del defensa.

        Returns:
            dict: Estadísticas del defensa (goles, asistencias, tarjetas,
            minutos jugados, goles en contra y pases completados).
        """
        return {
            "goles": self.__goles,
            "asistencias": self.__asistencias,
            "tarjetas_amarillas": self.__tarjetas_amarillas,
            "tarjetas_rojas": self.__tarjetas_rojas,
            "minutos_jugados": self.__minutos_jugados,
            "goles_en_contra": self.__goles_en_contra,
            "pases_completados" : self.__pases_completados
        }

