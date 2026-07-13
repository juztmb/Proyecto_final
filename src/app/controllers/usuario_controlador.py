from ..repository import UsuarioRepository
from ..models import usuario_factory
from ..repository import EquipoRepository
from ..models import EquipoFantasy

class UsuarioControlador:
    """Controlador encargado de la lógica de negocio de usuarios y equipos fantasy.

    Utiliza el patrón Factory (`usuario_factory`) para instanciar Clientes o
    Administradores según el token recibido, y gestiona la creación de
    equipos fantasy asociados a un usuario.

    Attributes:
        repository_usuario (UsuarioRepository): Acceso a datos de usuarios.
        reposiroty_equipo (EquipoRepository): Acceso a datos de equipos fantasy.
    """
    def __init__(self):
        """Inicializa el controlador con los repositorios de usuarios y equipos."""
        self.repository_usuario = UsuarioRepository()
        self.reposiroty_equipo = EquipoRepository()


    async def obtener_por_correo(self, body:dict):
        try:
            print(body)
            correo = body.get('correo',"")
            usuario = await self.repository_usuario.obtener_por_correo(correo)
            if usuario != None:
                print('entra a este')
                if usuario.get('contraseña') == body.get('contrasena'):
                    print('completa la validacion')
                    return {
                        'id': str(usuario["_id"]),
                        'correo': usuario.get('email')
                    }
                else:
                    return {
                        'correo': None ,
                        'contrasena': None
                        
                    }
                    
            else:
                print("usuario no existe")
                return { 'correo': None ,
                        'contrasena': None}
        except Exception as e:
            print("error", e)

    
    async def verificar_email(self, correo: str):
        try:
            print(correo)
            usuario = await self.repository_usuario.obtener_por_correo(correo)
            if usuario != None:
                return {
                    'existe' : True
                }
            else:
                return{
                    'existe': False
                }
        except Exception as e:
            print("error", e)

    async def crear(self, body:dict):
        """Crea un nuevo usuario (cliente o administrador) según el body recibido.

        Args:
            body (dict): Datos del usuario a crear (nombre, correo, contraseña, token, etc.).

        Returns:
            {'id': str} | {'id', None}: El id del usuario insertado, o None si ocurrió un error.
        """
        try:
            print(body)
            usuario = usuario_factory(body)
            info_usuario = await self.repository_usuario.crear(usuario.to_dict())
            return {'id': info_usuario}
        except Exception as e:
            print("error", e)
        
    async def crear_equipo(self, body:dict):
        """Crea un nuevo equipo fantasy para un usuario.

        Args:
            body (dict): Debe incluir "id_usuario" y "nombre_equipo".

        Returns:
            str | None: El id del equipo insertado, o None si ocurrió un error.
        """
        try:
            equipo = EquipoFantasy(id_usuario=body.get('id_usuario'),nombre_equipo=body.get('nombre_equipo'))
            return await self.reposiroty_equipo.crear(equipo.to_dict())
        except Exception as e:
            print('error', e)
    
    async def agregar_jugador_equipo(self, body:dict):
        """Agrega un jugador a un equipo fantasy existente, si aún no está en él.

        Args:
            body (dict): Debe incluir "equipo_id" y "jugador_id".

        Returns:
            int | None: Cantidad de documentos modificados, o None si el
            jugador ya estaba en el equipo o si ocurrió un error.
        """
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
        """Busca un usuario por su identificador.

        Args:
            usuario_id (str): Identificador del usuario.

        Returns:
            Usuarios | dict | None: Instancia reconstruida mediante el
            Factory, un diccionario vacío si no existe, o None si ocurre un error.
        """
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
        """Obtiene todos los usuarios registrados.

        Returns:
            list[dict] | None: Lista de usuarios.
        """
        try:
            return await self.repository_usuario.obtener_todos()
        except Exception as e:
            print(e)
    
    async def actualizar(self, body:dict):
        """Actualiza la información de un usuario existente.

        Args:
            body (dict): Debe incluir la clave "_id" y los campos a actualizar.

        Returns:
            int | None: Cantidad de documentos modificados.
        """
        try:
            usuario_id = body["_id"]
            del body["_id"]
            return await self.repository_usuario.actualizar(usuario_id,body)
        except Exception as e:
            print(e)
    
    async def eliminar(self, usuario_id: str):
        """Elimina un usuario de la base de datos.

        Args:
            usuario_id (str): Identificador del usuario a eliminar.

        Returns:
            int | None: Cantidad de documentos eliminados.
        """
        try:
            return await self.repository_usuario.eliminar(usuario_id)
        except Exception as e:
            print(e)

