class EquipoFantasy:
    def __init__(self, id_usuario, nombre_equipo, jugadores_en_equipo={}, puntos=0):
        self.__id_usuario = id_usuario
        self.__nombre_equipo = nombre_equipo
        self.__jugadores_en_equipo = jugadores_en_equipo
        self.__puntos = puntos

    def agregar_jugador(self, jugador_id):
        self.__jugadores_en_equipo[jugador_id] = {'puntos':0}
        
    def calcular_puntos(self):
        suma = 0
        for i in self.__jugadores_en_equipo:
            suma += i.get("puntos")

        self.__puntos = suma

    def to_dict(self) -> dict:
        data = {
            'id_usuario' : self.__id_usuario,
            'nombre_equipo' : self.__nombre_equipo,
            'jugadores_en_equipo': self.__jugadores_en_equipo,
            'puntos': self.__puntos
        }
        return data