from .usuarios import Usuarios


class Administrador(Usuarios):
    """
        Clase abstracta que representa la estructura de un administrador en la aplicacion.

        Attributes:
            nombre (str): Nombre del usuario en la aplicacion.
            email (str): Correo del usuario.
            contrasena (str): Contraseña del usuario.
            token (str) : Token que lo identifica como un administrador 
    """
    def __init__(self, nombre, email, contrasena):
        """
            Inicializa los atributos base del administrador.

            Args:
                nombre (str): Nombre del usuario en la aplicacion.
                email (str): Correo del usuario.
                contrasena (str): Contraseña del usuario.                
        """
        super().__init__(nombre, email, contrasena)
        self.__token = 'QWRtaW5pc3RyYWRvckFwbGljYWNpb24='

    def to_dict(self) -> dict:
        """
            Convierte los atributos base a diccionario.

            Returns:
                dict: Transforma toda la informacion del objeto a diccionario para ser guardada en la base de datos.
        """
        data = super().to_dict()
        data.update({
            "token": self.__token
        })
        return data