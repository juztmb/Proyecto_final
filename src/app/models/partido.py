from .rendimiento import Rendimiento

class Partido():
    """Representa un partido de fútbol simulado dentro de la liga fantasy.

    Agrupa la información general del encuentro (equipos, marcador,
    resultado) y mantiene la lista de identificadores de los rendimientos
    (`Rendimiento`) generados para los jugadores que participaron
    (relación de composición/agregación con `Rendimiento`).

    Attributes:
        id (str): Identificador del partido.
        fecha (str): Fecha en la que se disputó el partido.
        equipo_local (str): Nombre del equipo local.
        equipo_visitante (str): Nombre del equipo visitante.
        marcador_local (int): Goles anotados por el equipo local.
        marcador_visitante (int): Goles anotados por el equipo visitante.
        resultado (str): Resultado del partido.
        tiempo_extra (bool): Indica si el partido tuvo tiempo extra.
        penalties (bool): Indica si el partido se definió por penales.
        estadisticas_locales (dict): Estadísticas generales del equipo local.
        estadisticas_visitantes (dict): Estadísticas generales del equipo visitante.
    """
    def __init__(self, id, fecha, equipo_local, equipo_visitante, marcador_local, marcador_visitante, resultado, tiempo_extra, penalties, estadisticas_locales, estadisticas_visitantes):
        """Inicializa un partido con su información general.

        Args:
            id (str): Identificador del partido.
            fecha (str): Fecha del partido.
            equipo_local (str): Nombre del equipo local.
            equipo_visitante (str): Nombre del equipo visitante.
            marcador_local (int): Goles del equipo local.
            marcador_visitante (int): Goles del equipo visitante.
            resultado (str): Resultado del partido.
            tiempo_extra (bool): Si hubo tiempo extra.
            penalties (bool): Si se definió por penales.
            estadisticas_locales (dict): Estadísticas del equipo local.
            estadisticas_visitantes (dict): Estadísticas del equipo visitante.
        """
        self.__id = id
        self.__fecha = fecha
        self.__equipo_local = equipo_local
        self.__equipo_visitante = equipo_visitante
        self.__marcador_local = marcador_local
        self.__marcador_visitante = marcador_visitante
        self.__resultado = resultado
        self.__tiempo_extra = tiempo_extra
        self.__penalties = penalties
        self.__estadisticas_locales = estadisticas_locales
        self.__estadisticas_visitantes = estadisticas_visitantes
        self.__ID_rendimiento = []


    def agregar_ID_rendimiento(self, id_rendimiento):
        """Asocia el id de un rendimiento de jugador a este partido.

        Args:
            id_rendimiento (str): Identificador del `Rendimiento` generado
                para un jugador que participó en el partido.
        """
        self.__ID_rendimiento.append(id_rendimiento)
    
    def to_dict(self) -> dict:
        """
            Convierte los atributos base a diccionario.

            Returns:
                dict: Transforma toda la informacion del objeto a diccionario para ser guardada en la base de datos.
        """
        return {
            "_id": self.__id,
            "fecha": self.__fecha,
            "equipo_local": self.__equipo_local,
            "equipo_visitante": self.__equipo_visitante,
            "marcador_local": self.__marcador_local,
            "marcador_visitante": self.__marcador_visitante,
            "resultado": self.__resultado,
            "tiempo_extra": self.__tiempo_extra,
            "penalties": self.__penalties,
            "estadisticas_locales": self.__estadisticas_locales,
            "estadisticas_visitantes": self.__estadisticas_visitantes,
            "IDs_rendimiento": self.__ID_rendimiento
            
        }