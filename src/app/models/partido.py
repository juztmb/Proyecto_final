from .rendimiento import Rendimiento

class Partido():
    def __init__(self, id, fecha, equipo_local, equipo_visitante, marcador_local, marcador_visitante, resultado, tiempo_extra, penalties, estadisticas_locales, estadisticas_visitantes):
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