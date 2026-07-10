from .jugador import Jugador

class Medio(Jugador):
    """
        Clase abstracta que representa la estructura de un medio campista en la aplicacion.

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
            

    """
    def __init__(self, id, nombre, equipo, numero_camiseta, precio, puntos_jugador, tarjetas, goles, asistencias):
        """
            Inicializa los atributos base del medio campista.

            Args:
                id (str) : Id del jugador
                nombre (str): Nombre del usuario en la aplicacion.
                equipo (str): Correo del usuario.
                numero_camiseta (str)
                precio (float): precio del jugador
                puntos_jugador (float) : puntos del jugador segun estadisticas
                activo (bool): True si el jugador se encuentra activo
                tarjetas (dict): La cantidad de tarjetas amarillas y rojas que ha tenido durante la temporada
                goles (int): goles anotados en la temporada
                asistencias (int): asistencias hechas durante la temporada 
            
        """
        super().__init__(id, nombre, equipo, numero_camiseta, precio, puntos_jugador, tarjetas, goles, asistencias)
       

    def to_dict(self) -> dict:
        """
            Convierte los atributos base a diccionario.

            Returns:
                dict: Transforma toda la informacion del objeto a diccionario para ser guardada en la base de datos.
        """
        data = super().to_dict()
        data.update({
            "posicion": 'Medio',
        })
        return data