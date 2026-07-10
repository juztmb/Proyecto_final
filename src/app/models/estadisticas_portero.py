from .estadisticas_strategy import EstadisticasStrategy


class EstadisticasPortero(EstadisticasStrategy):
    def __init__(self, atajadas, goles, asistencias, tarjeta_amarilla, tarjeta_roja, minutos_juego, goles_en_contra):
        self.__atajadas = atajadas
        self.__goles = goles
        self.__asistencias = asistencias
        self.__tarjetas_amarillas = tarjeta_amarilla
        self.__tarjetas_rojas = tarjeta_roja
        self.__minutos_jugados = minutos_juego
        self.__goles_en_contra = goles_en_contra

    def calcular_puntos(self):
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
        return {
            "atajadas": self.__atajadas,
            "goles": self.__goles,
            "asistencias": self.__asistencias,
            "tarjetas_amarillas": self.__tarjetas_amarillas,
            "tarjetas_rojas": self.__tarjetas_rojas,
            "minutos_jugados": self.__minutos_jugados,
            "goles_en_contra": self.__goles_en_contra
        }

