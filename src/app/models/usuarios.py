class Usuarios():
    """
        Clase abstracta que representa la estructura  de un usuario en la aplicacion.

        Attributes:
            nombre (str): Nombre del usuario en la aplicacion.
            email (str): Correo del usuario.
            contrasena (str): Contraseña del usuario.
            
    """
    def __init__(self, nombre, email, contrasena):
        """
            Inicializa los atributos base del usuario, se hace una validacion para verificiar que el nombre, correo o contraseña no este vacio.

            Args:
                nombre (str): Nombre del usuario en la aplicacion.
                email (str): Correo del usuario.
                contrasena (str): Contraseña del usuario.
                
        """
        if not isinstance(nombre, str) or nombre.strip() == "":
            raise ValueError("El nombre debe ser un texto no vacío.")
        if not isinstance(email, str) or email.strip() == "":
            raise ValueError("El email debe ser un texto no vacío.")
        if not isinstance(contrasena, str) or contrasena.strip() == "":
            raise ValueError("La contraseña debe ser un texto no vacío.")
        
        self._nombre = nombre
        self._email = email
        self._contrasena = contrasena

    def to_dict(self) -> dict:
        """
            Convierte los atributos base a diccionario.

            Returns:
                dict: Transforma toda la informacion del objeto a diccionario para ser guardada en la base de datos.
        """
        return {
            "nombre": self._nombre,
            "email": self._email,
            "contraseña": self._contrasena,
            
        }
    
    def iniciar_sesion(self, email, contrasena):
        """
            Verifica si el email y la contrasena coinciden con lo que se tiene guardado.

            Args:
                email (str): Correo ingresado.
                contrasena (str): Contraseña ingresada.

            Returns:
                bool: True si la informacion ingresada coincide con el objeto.  
        """

        return self.email == email and self._contrasena == contrasena
    
    def cambiar_contraseña(self, nueva_contrasena):
        if isinstance(nueva_contrasena, str) and len(nueva_contrasena) > 5 and nueva_contrasena.strip() != "":
            self.__contrasena = nueva_contrasena
            