from ..repository import UsuarioRepository
from ..models import usuario_factory
from ..repository import EquipoRepository
from ..models import EquipoFantasy

class UsuarioControlador:
    def __init__(self):
        self.repository_usuario = UsuarioRepository()
        self.reposiroty_equipo = EquipoRepository()


    async def crear(self, body:dict):
        try:
            print(body)
            usuario = usuario_factory(body)
            return await self.repository_usuario.crear(usuario.to_dict())
        except Exception as e:
            print("error", e)
        
    async def crear_equipo(self, body:dict):
        try:
            equipo = EquipoFantasy(id_usuario=body.get('id_usuario'),nombre_equipo=body.get('nombre_equipo'))
            return await self.reposiroty_equipo.crear(equipo.to_dict())
        except Exception as e:
            print('error', e)
    
    async def agregar_jugador_equipo(self, body:dict):
        try:
            equipo_info = await self.reposiroty_equipo.obtener_por_id(equipo_id=body['equipo_id'])
            equipo_obj = EquipoFantasy(
                id_usuario=equipo_info["id_usuario"],
                nombre_equipo=equipo_info['equipo_id'],
                jugadores_en_equipo=equipo_info['jugadores_en_equipo'],
                puntos=equipo_info['puntos']
            )
            if equipo_info.get('jugadores_en_equipo',{}).get(body['jugador_id'], {})  == {}:
                equipo_obj.agregar_jugador(body['jugador_id'])
                return await self.reposiroty_equipo.actualizar(body['equipo_id'],equipo_obj.to_dict())
            else:
                print('El jugador ya se encuentra en el equipo')
                return None
        except Exception as e:
            print('error', e)

    async def obtener_por_id(self, usuario_id: str):
        try:
            usuario = await self.repository_usuario.obtener_por_id(usuario_id)
            print(usuario)
            if usuario == {}:
                return usuario
            else:
                return usuario_factory(usuario)
        except Exception as e:
            print(e)
    
    async def obtener_todos(self):
        try:
            return await self.repository_usuario.obtener_todos()
        except Exception as e:
            print(e)
    
    async def actualizar(self, body:dict):
        try:
            usuario_id = body["_id"]
            del body["_id"]
            return await self.repository_usuario.actualizar(usuario_id,body)
        except Exception as e:
            print(e)
    
    async def eliminar(self, usuario_id: str):
        try:
            return await self.repository_usuario.eliminar(usuario_id)
        except Exception as e:
            print(e)

