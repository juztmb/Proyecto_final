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
    def __init__(self):
        self.repository_partido = PartidoRepository()
        self.repository_jugador = JugadorRepository()
        self.repository_rendimiento = RendimientoRepository()
        self.repository_equipo = EquipoRepository()

    async def crear(self, body:dict):
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
        try:
            print(partido_id)
            partido = await self.repository_partido.obtener_por_id(partido_id)
            return partido
        except Exception as e:
            print(e)
    
    async def obtener_todos(self):
        try:
            return await self.repository_partido.obtener_todos()
        except Exception as e:
            print(e)
    
    async def actualizar(self, body:dict):
        try:
            partido_id = body["_id"]
            del body["_id"]
            return await self.repository_partido.actualizar(partido_id,body)
        except Exception as e:
            print(e)
    
    async def eliminar(self, partido_id: str):
        try:
            return await self.repository_partido.eliminar(partido_id)
        except Exception as e:
            print(e)



def armar_jugador(jugador_id, estadisticas, posicion, puntos):

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