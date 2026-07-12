from ..repository import PartidoRepository
from ..repository import JugadorRepository
from ..repository import RendimientoRepository
from ..repository import EquipoRepository
from .partido_controlador_notifier import PartidoControladorNotifier
from .puntos_equipo_controlador import PuntosEquipoControlador
from .puntos_jugador_controlador import PuntosJugadorControlador
from ..models import factory_estadisticas
from ..models import Partido
from ..models import Rendimiento



class PartidoControlador:
    """Controlador encargado de procesar y persistir los partidos simulados.

    Además de guardar el partido, calcula el rendimiento individual de cada
    jugador que participó (usando el patrón Strategy vía
    `factory_estadisticas`) y propaga los puntos obtenidos a los equipos
    fantasy y a los jugadores mediante el patrón Observer
    (`PartidoControladorNotifier`).

    Attributes:
        repository_partido (PartidoRepository): Acceso a datos de partidos.
        repository_jugador (JugadorRepository): Acceso a datos de jugadores.
        repository_rendimiento (RendimientoRepository): Acceso a datos de rendimiento.
        repository_equipo (EquipoRepository): Acceso a datos de equipos fantasy.
    """
    def __init__(self):
        """Inicializa el controlador instanciando los repositorios necesarios
        para procesar un partido (partidos, jugadores, rendimiento y equipos).
        """
        self.repository_partido = PartidoRepository()
        self.repository_jugador = JugadorRepository()
        self.repository_rendimiento = RendimientoRepository()
        self.repository_equipo = EquipoRepository()

    async def crear(self, body:dict):
        """Procesa el resultado final de un partido y genera los rendimientos.

        Solo procesa partidos cuyo estado sea "finished". El flujo es:
            1. Construye el objeto `Partido` con la información general.
            2. Contabiliza goles, tarjetas y sustituciones por equipo.
            3. Para cada jugador en las alineaciones, calcula minutos jugados
               y arma sus estadísticas generales del partido.
            4. Genera las estadísticas específicas por posición (Strategy) y
               calcula los puntos obtenidos (`Rendimiento`).
            5. Notifica (Observer) a los controladores de puntos de equipo y
               de jugador para que actualicen sus totales.

        Args:
            body (dict): Payload con la información completa del partido
                (equipos, marcador, goles, tarjetas, sustituciones, alineaciones
                y estadísticas por equipo).

        Returns:
            str | None: El id del partido insertado, o None si el partido no
            está finalizado o si ocurrió un error durante el procesamiento.
        """
        if body['status'] == 'finished':

            try:
                
                partido = Partido(
                    id=body['id'],
                    fecha=body['date'],
                    equipo_local=body['homeTeam'],
                    equipo_visitante=body['awayTeam'],
                    marcador_local=body['homeScore'],
                    marcador_visitante=body['awayScore'],
                    resultado=body['result'],
                    tiempo_extra=body['extraTime'],
                    penalties=body['penalties'],
                    estadisticas_locales=body['statistics']['home'],
                    estadisticas_visitantes=body['statistics']['away']
                )
                
                goles={ 'home': {}, 'away': {}}
                for i in body['goals']:
                    if i.get('team') == 'home':
                        if i.get('type') == None:
                            anotador = i.get('scorer')
                            if goles['home'].get(anotador) != None:
                                goles['home'][anotador] += 1
                            else:
                                goles['home'][anotador] = 1
                    elif i.get('team') == 'away':
                        if i.get('type')== None:
                            anotador = i.get('scorer')
                            if goles['away'].get(anotador) != None:
                                goles['away'][anotador] += 1
                            else:
                                goles['away'][anotador] = 1
 

                tarjetas={ 'home':{}, 'away':{}}
                for i in body['cards']:
                    if i.get('team') == 'home':

                        tarjeta_jugador = i.get('player')
                        color_tarjeta = i.get('color')

                        if tarjetas['home'].get(tarjeta_jugador) != None:
                            if color_tarjeta == 'yellow':
                                tarjetas['home'][tarjeta_jugador]['amarilla'] += 1
                            elif color_tarjeta == 'red':
                                tarjetas['home'][tarjeta_jugador]['roja'] += 1
                        else:
                            if color_tarjeta == 'yellow':
                                tarjetas['home'][tarjeta_jugador] = {'amarilla':1,'roja':0}
                            elif color_tarjeta == 'red':
                                tarjetas['home'][tarjeta_jugador] = {'amarilla':0, 'roja': 1}

                    elif i.get('team') == 'away':

                        tarjeta_jugador = i.get('player')
                        color_tarjeta = i.get('color')

                        if tarjetas['away'].get(tarjeta_jugador) != None:
                            if color_tarjeta == 'yellow':
                                tarjetas['away'][tarjeta_jugador]['amarilla'] += 1
                            elif color_tarjeta == 'red':
                                tarjetas['away'][tarjeta_jugador]['roja'] += 1
                        else:
                            if color_tarjeta == 'yellow':
                                tarjetas['away'][tarjeta_jugador] = {'amarilla':1,'roja':0}
                            elif color_tarjeta == 'red':
                                tarjetas['away'][tarjeta_jugador] = {'amarilla':0, 'roja': 1}

                sustitucion = {'home':{'entra':{},'sale':{}},'away':{'entra':{},'sale':{}}}

                for i in body['substitutions']:
                    if i.get('team') == 'home':
                        jugador_entrante = i.get('on')
                        jugador_saliente = i.get('off')
                        sustitucion['home']['entra'][jugador_entrante] = i.get('minute')
                        sustitucion['home']['sale'][jugador_saliente] = i.get('minute')
                    elif i.get('team') == 'away':
                        jugador_entrante = i.get('on')
                        jugador_saliente = i.get('off')
                        sustitucion['away']['entra'][jugador_entrante] = i.get('minute')
                        sustitucion['away']['sale'][jugador_saliente] = i.get('minute')

                for team in ['home', 'away']:
                    for jugador in body['lineups'][team]:
                        jugador_info = await self.repository_jugador.obtener_por_nombre(jugador['player'])
                        nombre, apellido = jugador_info.get('nombre').split()
                        minutos_juego = 0
                        goles_en_contra = 0
                        if team == 'home':
                            goles_en_contra = body['awayScore']
                        elif team == 'away':
                            goles_en_contra = body['homeScore']
                        
                        if jugador.get('starter') == True:
                            if sustitucion.get(team).get('sale').get(jugador_info.get('nombre')) != None:
                                minutos_juego = sustitucion.get(team).get('sale').get(jugador_info.get('nombre'))
                            elif body['extraTime'] == False:
                                minutos_juego = 90
                            elif body['extraTime'] == True:
                                minutos_juego = 120
                        else:
                            if sustitucion.get(team).get('entra').get(jugador_info.get('nombre')) != None and body['extraTime'] == False:
                                minutos_juego = 90 - sustitucion.get(team).get('entra').get(jugador_info.get('nombre'))
                            elif sustitucion.get(team).get('entra').get(jugador_info.get('nombre'))!= None and body['extraTime'] == True:
                                minutos_juego = 120 - sustitucion.get(team).get('entra').get(jugador_info.get('nombre'))


                        estadisticas_generales = {
                            'atajadas': body['statistics'].get(team,0).get('goalkeeperSaves',0),
                            'goles': goles.get(team,0).get(apellido,0),
                            'asistencias': 0,
                            'tarjetas_amarillas': tarjetas.get(team,0).get(jugador_info.get('nombre'),{}).get('amarilla',0),
                            'tarjetas_rojas': tarjetas.get(team,0).get(jugador_info.get('nombre'),{}).get('roja',0),
                            'minutos_juego': minutos_juego,
                            'goles_en_contra': goles_en_contra,
                            'pases_completados': body['statistics'].get(team,0).get('passesAccurate'),
                            'tiros_a_puerta': body['statistics'].get(team,0).get('shotsTotal')
                            

                        }

                        est_strategy = factory_estadisticas(jugador_info.get('posicion'),estadisticas_generales)
                        rendimiento = Rendimiento(
                            jugador_id=jugador_info.get('_id'),
                            partido_id=body['id'],
                            estadisticas_strategy= est_strategy

                            )
                        rendimiento.calcular_puntos()
                        id_rendimiento = await self.repository_rendimiento.crear(rendimiento.to_dict())
                        partido.agregar_ID_rendimiento(id_rendimiento)
                        jugador_actualizar = armar_jugador(jugador_info.get('_id'), est_strategy.obtener_estadisticas(),jugador_info.get('posicion'), est_strategy.calcular_puntos())
                        partido_notifier = PartidoControladorNotifier()
                        puntos_equipo = PuntosEquipoControlador(self.repository_equipo)
                        puntos_jugador = PuntosJugadorControlador(self.repository_jugador)

                        partido_notifier.attach(puntos_equipo)
                        partido_notifier.attach(puntos_jugador)
                        await partido_notifier.notificar(jugador_actualizar)
                        print(jugador_actualizar)


                return await self.repository_partido.crear(partido.to_dict())
            except Exception as e:
                print("error", e)
                return None
        else:
            print('El partido, no esta finalizado')
            return None

       
    async def obtener_por_id(self, partido_id: str):
        """Busca un partido por su identificador.

        Args:
            partido_id (str): Identificador del partido.

        Returns:
            dict | None: Documento del partido encontrado.
        """
        try:
            print(partido_id)
            partido = await self.repository_partido.obtener_por_id(partido_id)
            return partido
        except Exception as e:
            print(e)
    
    async def obtener_todos(self):
        """Obtiene todos los partidos registrados.

        Returns:
            list[dict] | None: Lista de partidos.
        """
        try:
            return await self.repository_partido.obtener_todos()
        except Exception as e:
            print(e)
    
    async def actualizar(self, body:dict):
        """Actualiza la información de un partido existente.

        Args:
            body (dict): Debe incluir la clave "_id" con el identificador del
                partido y el resto de campos a actualizar.

        Returns:
            int | None: Cantidad de documentos modificados.
        """
        try:
            partido_id = body["_id"]
            del body["_id"]
            return await self.repository_partido.actualizar(partido_id,body)
        except Exception as e:
            print(e)
    
    async def eliminar(self, partido_id: str):
        """Elimina un partido de la base de datos.

        Args:
            partido_id (str): Identificador del partido a eliminar.

        Returns:
            int | None: Cantidad de documentos eliminados.
        """
        try:
            return await self.repository_partido.eliminar(partido_id)
        except Exception as e:
            print(e)



def armar_jugador(jugador_id, estadisticas, posicion, puntos):
    """Construye el diccionario de actualización de un jugador tras un partido.

    Se usa como paso previo a notificar (Observer) a los controladores que
    actualizan los puntos del jugador y de los equipos fantasy que lo tienen.

    Args:
        jugador_id (str): Identificador del jugador.
        estadisticas (dict): Estadísticas obtenidas del partido (goles,
            asistencias, tarjetas, atajadas, etc.).
        posicion (str): Posición del jugador ("Portero", "Defensa",
            "Medio" o "Delantero").
        puntos (float): Puntos totales calculados para el jugador en el partido.

    Returns:
        dict: Diccionario con la información resumida del jugador lista para
        ser enviada a los observadores.
    """
    if posicion == 'Portero':
        return {
            "_id": jugador_id,
            "atajadas" : estadisticas.get('atajadas'),
            "goles": estadisticas.get('goles'),
            "asistencias": estadisticas.get('asistencias'),
            'tarjetas': {
                'amarillas': estadisticas.get('tarjetas_amarillas'),
                'rojas': estadisticas.get('tarjetas_rojas')
            },
            "puntos": puntos
        }
    else:
        return {
            "_id": jugador_id,
            "atajadas" : estadisticas.get('atajadas'),
            "goles": estadisticas.get('goles'),
            "asistencias": estadisticas.get('asistencias'),
            'tarjetas': {
                'amarillas': estadisticas.get('tarjetas_amarillas'),
                'rojas': estadisticas.get('tarjetas_rojas')
            },
            "puntos": puntos
        }