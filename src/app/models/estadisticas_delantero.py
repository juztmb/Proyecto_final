from .estadisticas_strategy import EstadisticasStrategy


class EstadisticasDelantero(EstadisticasStrategy):
    """Estrategia de cálculo de puntos para la posición de Delantero.

    Pondera principalmente los goles y los tiros a puerta, ya que su rol
    ofensivo es la principal fuente de puntos.

    Attributes:
        goles (int): Goles anotados.
        asistencias (int): Asistencias realizadas.
        tarjetas_amarillas (int): Tarjetas amarillas recibidas.
        tarjetas_rojas (int): Tarjetas rojas recibidas.
        minutos_jugados (int): Minutos jugados en el partido.
        pases_completados (int): Pases completados durante el partido.
        tiros_a_puerta (int): Tiros a puerta realizados.
    """
    def __init__(self, goles, asistencias, tarjeta_amarilla, tarjeta_roja, minutos_juego, pases_completados, tiros_a_puerta):
        """Inicializa las estadísticas del delantero para un partido.

        Args:
            goles (int): Goles anotados.
            asistencias (int): Asistencias realizadas.
            tarjeta_amarilla (int): Tarjetas amarillas recibidas.
            tarjeta_roja (int): Tarjetas rojas recibidas.
            minutos_juego (int): Minutos jugados.
            pases_completados (int): Pases completados en el partido.
            tiros_a_puerta (int): Tiros a puerta realizados.
        """
        self.__goles = goles
        self.__asistencias = asistencias
        self.__tarjetas_amarillas = tarjeta_amarilla
        self.__tarjetas_rojas = tarjeta_roja
        self.__minutos_jugados = minutos_juego
        self.__pases_completados = pases_completados
        self.__tiros_a_puerta = tiros_a_puerta

    def calcular_puntos(self):
        """Calcula los puntos fantasy del delantero.

        Reglas aplicadas: +4 por gol, +3 por asistencia, -2 por tarjeta
        amarilla, -5 por tarjeta roja, +1 o +2 por minutos jugados
        (≤60 / >60), +1 por cada 15 pases completados, y +1 por cada tiro
        a puerta.

        Returns:
            float: Puntos totales obtenidos por el delantero en el partido.
        """
        puntos = 0
        puntos += (self.__goles) * 4
        puntos += (self.__asistencias) * 3
        puntos -= (self.__tarjetas_amarillas) * 2
        puntos -= (self.__tarjetas_rojas) * 5
        if self.__minutos_jugados <= 60:
            puntos += 1
        elif self.__minutos_jugados >60:
            puntos += 2
        else:
            puntos +=0
        
        puntos += (self.__pases_completados//15) * 1
        puntos += (self.__tiros_a_puerta) * 1
        return puntos 

    def obtener_estadisticas(self):
        """Devuelve las estadísticas crudas del delantero.

        Returns:
            dict: Estadísticas del delantero (goles, asistencias, tarjetas,
            minutos jugados, pases completados y tiros a puerta).
        """
        return {
            "goles": self.__goles,
            "asistencias": self.__asistencias,
            "tarjetas_amarillas": self.__tarjetas_amarillas,
            "tarjetas_rojas": self.__tarjetas_rojas,
            "minutos_jugados": self.__minutos_jugados,
            "pases_completados" : self.__pases_completados,
            "tiros_a_puerta" : self.__tiros_a_puerta
        }

