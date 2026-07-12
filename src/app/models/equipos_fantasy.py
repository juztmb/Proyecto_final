class EquipoFantasy:
    """Representa un equipo fantasy creado por un usuario/cliente.

    Un equipo agrupa jugadores reales (por id) y acumula los puntos que
    estos obtienen partido a partido.

    Attributes:
        id_usuario (str): Identificador del usuario dueño del equipo.
        nombre_equipo (str): Nombre del equipo fantasy.
        jugadores_en_equipo (dict): Diccionario {jugador_id: {"puntos": int}}
            con los jugadores fichados y sus puntos acumulados.
        puntos (int): Puntos totales acumulados por el equipo.
    """
    def __init__(self, id_usuario, nombre_equipo, jugadores_en_equipo={}, puntos=0):
        """Inicializa un equipo fantasy.

        Args:
            id_usuario (str): Identificador del usuario dueño del equipo.
            nombre_equipo (str): Nombre del equipo fantasy.
            jugadores_en_equipo (dict, opcional): Jugadores ya fichados.
                Por defecto un diccionario vacío.
            puntos (int, opcional): Puntos iniciales del equipo. Por defecto 0.
        """
        self.__id_usuario = id_usuario
        self.__nombre_equipo = nombre_equipo
        self.__jugadores_en_equipo = jugadores_en_equipo
        self.__puntos = puntos

    def agregar_jugador(self, jugador_id):
        """Ficha un jugador para el equipo (mercado de fichajes).

        Args:
            jugador_id (str): Identificador del jugador a agregar al equipo.
        """
        self.__jugadores_en_equipo[jugador_id] = {'puntos':0}
        
    def calcular_puntos(self):
        """Recalcula el total de puntos del equipo sumando los puntos de
        cada jugador en la plantilla.
        """
        suma = 0
        for i in self.__jugadores_en_equipo:
            suma += i.get("puntos")

        self.__puntos = suma

    def to_dict(self) -> dict:
        """Convierte el equipo a diccionario para persistirlo en la base de datos.

        Returns:
            dict: Representación del equipo fantasy.
        """
        data = {
            'id_usuario' : self.__id_usuario,
            'nombre_equipo' : self.__nombre_equipo,
            'jugadores_en_equipo': self.__jugadores_en_equipo,
            'puntos': self.__puntos
        }
        return data