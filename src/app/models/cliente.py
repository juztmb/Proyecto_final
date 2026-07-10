from .usuarios import Usuarios

# Clase hija de la clase usuarios especializado para los que van a crear equipos y acumular puntos


class Cliente(Usuarios):
    """
        Clase abstracta que representa la estructura de un cliente en la aplicacion.

        Attributes:
            nombre (str): Nombre del usuario en la aplicacion.
            email (str): Correo del usuario.
            contrasena (str): Contraseña del usuario.
            puntos_totales (dict) : diccionarios con la informacion de los puntos obtenidos durante cada fase
            nombre_usuario (str): nombre que se ve dentro de la pagina
            equipos (list[str]) : lista con los equipos creados por el usuario

            
    """
    def __init__(self, nombre, email, contrasena, puntos_totales, nombre_usuario, equipos):
        super().__init__(nombre, email, contrasena)
        """
            Inicializa los atributos base del usuario, se hace una validacion para verificiar que el nombre de usuario no este vacio.

            Args:
                nombre (str): Nombre del usuario en la aplicacion.
                email (str): Correo del usuario.
                contrasena (str): Contraseña del usuario.
                
        """
        if not isinstance(nombre_usuario, str) or nombre.strip() == "":
            raise ValueError("El nombre de usuario debe ser un texto no vacío.")
        if not isinstance(puntos_totales, dict):
            raise ValueError("Los puntos totales no tienen el formato correcto")
        if not isinstance(equipos, list):
            raise ValueError("Los equipos no tienen el formato correcto")
        
        self.__nombre_usuario = nombre_usuario
        self.__puntos_totales = puntos_totales
        self.__equipos = equipos
        self.__token = "NA"
    
    def to_dict(self) -> dict:
        """
            Convierte los atributos base a diccionario.

            Returns:
                dict: Transforma toda la informacion del objeto a diccionario para ser guardada en la base de datos.
        """
        data = super().to_dict()
        data.update({
            "nombre_usuario": self.__nombre_usuario,
            "puntos_totales" : self.__puntos_totales,
            "equipos" : self.__equipos,
            "token": self.__token
        })
        return data
    

