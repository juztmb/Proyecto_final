from .estadisticas_strategy import EstadisticasStrategy


class EstadisticasMedio(EstadisticasStrategy):
    """Estrategia de cálculo de puntos para la posición de Mediocampista.

    Combina factores ofensivos (goles, asistencias, tiros a puerta) con
    factores defensivos (portería en cero del equipo), reflejando el rol
    mixto de esta posición.

    Attributes:
        goles (int): Goles anotados.
        asistencias (int): Asistencias realizadas.
        tarjetas_amarillas (int): Tarjetas amarillas recibidas.
        tarjetas_rojas (int): Tarjetas rojas recibidas.
        minutos_jugados (int): Minutos jugados en el partido.
        goles_en_contra (int): Goles recibidos por su equipo mientras jugaba.
        pases_completados (int): Pases completados durante el partido.
        tiros_a_puerta (int): Tiros a puerta realizados.
    """
    def __init__(self, goles, asistencias, tarjeta_amarilla, tarjeta_roja, minutos_juego, goles_en_contra, pases_completados, tiros_a_puerta):
        """Inicializa las estadísticas del mediocampista para un partido.

        Args:
            goles (int): Goles anotados.
            asistencias (int): Asistencias realizadas.
            tarjeta_amarilla (int): Tarjetas amarillas recibidas.
            tarjeta_roja (int): Tarjetas rojas recibidas.
            minutos_juego (int): Minutos jugados.
            goles_en_contra (int): Goles recibidos mientras jugaba.
            pases_completados (int): Pases completados en el partido.
            tiros_a_puerta (int): Tiros a puerta realizados.
        """
        self.__goles = goles
        self.__asistencias = asistencias
        self.__tarjetas_amarillas = tarjeta_amarilla
        self.__tarjetas_rojas = tarjeta_roja
        self.__minutos_jugados = minutos_juego
        self.__goles_en_contra = goles_en_contra
        self.__pases_completados = pases_completados
        self.__tiros_a_puerta = tiros_a_puerta

    def calcular_puntos(self):
        """Calcula los puntos fantasy del mediocampista.

        Reglas aplicadas: +5 por gol, +3 por asistencia, -2 por tarjeta
        amarilla, -5 por tarjeta roja, +1 o +2 por minutos jugados
        (≤60 / >60), +1 si termina con portería en cero habiendo jugado
        60+ minutos, +1 por cada 15 pases completados, y +1 por cada tiro
        a puerta.

        Returns:
            float: Puntos totales obtenidos por el mediocampista en el partido.
        """
        puntos = 0
        puntos += (self.__goles) * 5
        puntos += (self.__asistencias) * 3
        puntos -= (self.__tarjetas_amarillas) * 2
        puntos -= (self.__tarjetas_rojas) * 5
        if self.__minutos_jugados <= 60:
            puntos += 1
        elif self.__minutos_jugados >60:
            puntos += 2
        else:
            puntos +=0

        if self.__goles_en_contra == 0 and self.__minutos_jugados >=60:
            puntos += 1 
        
        puntos += (self.__pases_completados//15) * 1
        puntos += (self.__tiros_a_puerta) * 1
        return puntos 

    def obtener_estadisticas(self):
        """Devuelve las estadísticas crudas del mediocampista.

        Returns:
            dict: Estadísticas del mediocampista (goles, asistencias,
            tarjetas, minutos jugados, goles en contra, pases completados
            y tiros a puerta).
        """
        return {
            "goles": self.__goles,
            "asistencias": self.__asistencias,
            "tarjetas_amarillas": self.__tarjetas_amarillas,
            "tarjetas_rojas": self.__tarjetas_rojas,
            "minutos_jugados": self.__minutos_jugados,
            "goles_en_contra": self.__goles_en_contra,
            "pases_completados" : self.__pases_completados,
            "tiros_a_puerta" : self.__tiros_a_puerta
        }

