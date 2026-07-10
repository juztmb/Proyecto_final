from .portero import Portero
from .defensa import Defensa
from .delantero import Delantero
from .medio import Medio
from .jugador import Jugador


def jugador_factory(doc: dict):
    """
     Funcion encargada de crear los jugadores dependiendo de su posicion
    """
    if not doc:
        return None
     
    posicion = doc.get("posicion")
    print(posicion)
    if posicion == "Portero":
        return Portero(
            id=doc["_id"],
            nombre=doc["nombre"],
            equipo=doc["equipo"],
            numero_camiseta=doc["numero_camiseta"],
            precio=doc["precio"],
            puntos_jugador=doc["puntos_jugador"],
            tarjetas=doc["tarjetas"],
            goles=doc["goles"],
            asistencias=doc["asistencias"],
            porteria_cero=doc["porteria_cero"],
            atajadas=doc["atajadas"]
        )
    elif posicion == "Delantero":
        return Delantero(
            id=doc["_id"],
            nombre=doc["nombre"],
            equipo=doc["equipo"],
            numero_camiseta=doc["numero_camiseta"],
            precio=doc["precio"],
            puntos_jugador=doc["puntos_jugador"],
            tarjetas=doc["tarjetas"],
            goles=doc["goles"],
            asistencias=doc["asistencias"]
        )
    elif posicion == "Medio":
        return Medio(
            id=doc["_id"],
            nombre=doc["nombre"],
            equipo=doc["equipo"],
            numero_camiseta=doc["numero_camiseta"],
            precio=doc["precio"],
            puntos_jugador=doc["puntos_jugador"],
            tarjetas=doc["tarjetas"],
            goles=doc["goles"],
            asistencias=doc["asistencias"]
        )
    elif posicion == "Defensa":
        return Defensa(
            id=doc["_id"],
            nombre=doc["nombre"],
            equipo=doc["equipo"],
            numero_camiseta=doc["numero_camiseta"],
            precio=doc["precio"],
            puntos_jugador=doc["puntos_jugador"],
            tarjetas=doc["tarjetas"],
            goles=doc["goles"],
            asistencias=doc["asistencias"],
            porteria_cero=doc["porteria_cero"],
        )
    else:
        return Jugador(
            id=doc["_id"],
            nombre=doc["nombre"],
            equipo=doc["equipo"],
            goles=doc["goles"]
        )
