from .jugador import Jugador


class Defensa(Jugador):
    """
        Clase abstracta que representa la estructura de un defensa en la aplicacion.

        Attributes:
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
            porteria_cero (int): veces en las que el partido termino con cero goles en contra
            goles_en_contra(int): veces en las que el jugador recibio un gol 

    """
    def __init__(self, id, nombre, equipo, numero_camiseta, precio, puntos_jugador, tarjetas, goles, asistencias, porteria_cero):
        """
            Inicializa los atributos base del defensa.

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
                porteria_cero (int): veces en las que el partido termino con cero goles en contra
        """
        super().__init__(id, nombre, equipo, numero_camiseta, precio, puntos_jugador, tarjetas, goles, asistencias)
        self.__porteria_cero = porteria_cero

    def to_dict(self) -> dict:
        """
            Convierte los atributos base a diccionario.

            Returns:
                dict: Transforma toda la informacion del objeto a diccionario para ser guardada en la base de datos.
        """
        data = super().to_dict()
        data.update({
            "posicion": 'Defensa',
            "porteria_cero": self.__porteria_cero,
        })
        return data