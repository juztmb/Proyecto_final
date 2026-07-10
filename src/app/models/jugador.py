class Jugador():
    """
        Clase abstracta que representa la estructura de un jugador en la aplicacion.

        Attributes:
            id (str) : Id del jugador
            nombre (str): Nombre del jugador.
            equipo (str): Equipo del jugador.
            numero_camiseta (str)
            precio (float): precio del jugador
            puntos_jugador (float) : puntos del jugador segun estadisticas
            activo (bool): True si el jugador se encuentra activo
            tarjetas (dict): La cantidad de tarjetas amarillas y rojas que ha tenido durante la temporada.
            goles (int): goles anotados en la temporada
            asistencias (int): asistencias hechas durante la temporada
    """
    def __init__(self, id, nombre, equipo, numero_camiseta, precio, puntos_jugador, tarjetas, goles, asistencias):
        """
            Inicializa los atributos base del administrador.

            Args:
                id (str) : Id del jugador
                nombre (str): Nombre del jugador.
                equipo (str): Equipo del jugador.
                numero_camiseta (str)
                precio (float): precio del jugador
                puntos_jugador (float) : puntos del jugador segun estadisticas
                activo (bool): True si el jugador se encuentra activo
                tarjetas (dict): La cantidad de tarjetas amarillas y rojas que ha tenido durante la temporada
                goles (int): goles anotados en la temporada
                asistencias (int): asistencias hechas durante la temporada 
                
        """
        self.__id = id
        self.__nombre = nombre
        self.__equipo = equipo
        self.__numero_camiseta = numero_camiseta
        self.__precio = precio
        self.__puntos_jugador = puntos_jugador
        self.__tarjetas = tarjetas
        self.__activo = True
        self.__goles = goles
        self.__asistencias = asistencias

    def to_dict(self) -> dict:
        """
            Convierte los atributos base a diccionario.

            Returns:
                dict: Transforma toda la informacion del objeto a diccionario para ser guardada en la base de datos.
        """
        return {
            "_id": self.__id,
            "nombre": self.__nombre,
            "equipo": self.__equipo,
            "numero_camiseta": self.__numero_camiseta,
            "posicion": "General",
            "precio": self.__precio,
            "puntos_jugador": self.__puntos_jugador,
            "tarjetas": self.__tarjetas,
            "activo": self.__activo,
            "goles": self.__goles,
            "asistencias": self.__asistencias
        }
