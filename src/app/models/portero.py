from .jugador import Jugador


class Portero(Jugador):
    """
        Clase abstracta que representa la estructura de un portero en la aplicacion.

        Attributes:
            id (str) : Id del jugador
            nombre (str): Nombre del jugador.
            equipo (str): Equipo del jugador.
            numero_camiseta (str): numero de la camiseta
            precio (float): precio del jugador
            puntos_jugador (float) : puntos del jugador segun estadisticas
            activo (bool): True si el jugador se encuentra activo
            tarjetas (dict): La cantidad de tarjetas amarillas y rojas que ha tenido durante la temporada 
            goles (int): goles anotados en la temporada
            asistencias (int): asistencias hechas durante la temporada
            porteria_cero (int): veces en las que el partido termino con cero goles en contra
            atajadas (int): veces que el portero atajo un balon durante la temporada

    """
    def __init__(self, id, nombre, equipo, numero_camiseta, precio, puntos_jugador, tarjetas, goles, asistencias, porteria_cero, atajadas):
        """
            Inicializa los atributos base del defensa.

            Args:
                id (str) : Id del jugador
                nombre (str): Nombre del jugador.
                equipo (str): Equipo del jugador.
                numero_camiseta (str): Numero de la camiseta.
                precio (float): precio del jugador
                puntos_jugador (float) : puntos del jugador segun estadisticas
                activo (bool): True si el jugador se encuentra activo
                tarjetas (dict): La cantidad de tarjetas amarillas y rojas que ha tenido durante la temporada
                goles (int): goles anotados en la temporada
                asistencias (int): asistencias hechas durante la temporada 
                porteria_cero (int): veces en las que el partido termino con cero goles en contra
                atajadas (int): veces que el portero atajo un balon durante la teemporada
                
        """
        super().__init__(id, nombre, equipo, numero_camiseta, precio, puntos_jugador, tarjetas, goles, asistencias)
        self.__porteria_cero = porteria_cero
        self.__atajadas = atajadas

    def to_dict(self) -> dict:
        """
            Convierte los atributos base a diccionario.

            Returns:
                dict: Transforma toda la informacion del objeto a diccionario para ser guardada en la base de datos.
        """
        data = super().to_dict()
        data.update({
            "posicion": 'Portero',
            "porteria_cero": self.__porteria_cero,
            "atajadas": self.__atajadas
        })
        return data