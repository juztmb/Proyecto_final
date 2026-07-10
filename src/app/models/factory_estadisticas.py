from .estadisticas_portero import EstadisticasPortero
from .estadisticas_defensa import EstadisticasDefensa
from .estadisticas_delantero import EstadisticasDelantero
from .estadisticas_medio import EstadisticasMedio


def factory_estadisticas(posicion: str, doc: dict):
    """
     Funcion encargada de crear las estadisticas dependiendo de su posicion
    """
    if not doc:
        return None
     
    print(posicion)
    if posicion == "Portero":
        return EstadisticasPortero(
            atajadas=doc["atajadas"],
            goles=doc["goles"],
            asistencias=doc["asistencias"],
            tarjeta_amarilla=doc["tarjetas_amarillas"],
            tarjeta_roja=doc['tarjetas_rojas'],
            minutos_juego=doc['minutos_juego'],
            goles_en_contra=doc['goles_en_contra']
        )
    elif posicion == "Delantero":
        return EstadisticasDelantero(
            goles=doc["goles"],
            asistencias=doc["asistencias"],
            tarjeta_amarilla=doc["tarjetas_amarillas"],
            tarjeta_roja=doc['tarjetas_rojas'],
            minutos_juego=doc['minutos_juego'],
            pases_completados=doc["pases_completados"],
            tiros_a_puerta=doc["tiros_a_puerta"]
        )
    elif posicion == "Medio":
        return EstadisticasMedio(
            goles=doc["goles"],
            asistencias=doc["asistencias"],
            tarjeta_amarilla=doc["tarjetas_amarillas"],
            tarjeta_roja=doc['tarjetas_rojas'],
            minutos_juego=doc['minutos_juego'],
            goles_en_contra=doc['goles_en_contra'],
            pases_completados=doc["pases_completados"],
            tiros_a_puerta=doc["tiros_a_puerta"]

        )
    elif posicion == "Defensa":
        return EstadisticasDefensa(
            goles=doc["goles"],
            asistencias=doc["asistencias"],
            tarjeta_amarilla=doc["tarjetas_amarillas"],
            tarjeta_roja=doc['tarjetas_rojas'],
            minutos_juego=doc['minutos_juego'],
            goles_en_contra=doc['goles_en_contra'],
            pases_completados=doc["pases_completados"]
        )
    else:
        return {

        }
