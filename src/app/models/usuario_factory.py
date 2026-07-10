from .cliente import Cliente
from .admin import Administrador
from .usuarios import Usuarios


def usuario_factory(doc: dict):
    """
     Funcion encargada de crear los jugadores dependiendo de su posicion
    """
    if not doc:
        return None
     
    token = doc.get("token")
    print()
    if token == "QWRtaW5pc3RyYWRvckFwbGljYWNpb24":
        return Administrador(
            nombre=doc["nombre"],
            email=doc["correo"],
            contrasena=doc["contrasena"]
        )
    elif token == "NA":
        return Cliente(
            nombre=doc["nombre"],
            email=doc["correo"],
            contrasena=doc["contrasena"],
            nombre_usuario=doc['nombre_usuario']
            puntos_totales={},
            equipos=[]
        )
    else:
        return Usuarios(
            nombre=doc["nombre"],
            email=doc["email"],
            contrasena=doc["contrasena"]
        )
