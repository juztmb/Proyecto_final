from ..repository import UsuarioRepository
from ..models import usuario_factory
from ..repository import EquipoRepository
from ..models import EquipoFantasy
from ..repository import JugadorRepository
from fastapi import FastAPI, HTTPException, status
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
        self.repository_jugador = JugadorRepository()

    async def obtener_por_correo(self, body:dict):
        """
            Verifica si ya existe un usuario registrado con el correo electrónico dado.

            Args:
                correo (str): Dirección de correo electrónico a verificar.

            Returns:
                dict: Diccionario indicando si el correo existe, con la forma:
                    {'existe': True}  -> si se encontró un usuario con ese correo.
                    {'existe': False} -> si no se encontró ningún usuario con ese correo.
                Retorna None si ocurre una excepción durante la consulta.

        """
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
                        'correo': usuario.get('email'),
                        'nombre_usuario': usuario.get('nombre_usuario')
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
        """
            Verifica si ya existe un usuario registrado con el correo electrónico dado.

            Args:
                correo (str): Dirección de correo electrónico a verificar.

            Returns:
                dict: Diccionario indicando si el correo existe, con la forma:
                    {'existe': True}  -> si se encontró un usuario con ese correo.
                    {'existe': False} -> si no se encontró ningún usuario con ese correo.
                Retorna None si ocurre una excepción durante la consulta.

        """

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

    async def obtener_equipos(self, usuario_id: str):
        """
            Obtiene la lista de equipos asociados a un usuario específico.

            Args:
                usuario_id (str): Identificador del usuario del cual se quieren
                    obtener los equipos.

            Returns:
                list[dict]: Lista de diccionarios con los datos de cada equipo,
                    con las siguientes claves:
                        - id (str): Identificador del equipo (ObjectId convertido a str).
                        - name (str): Nombre del equipo.
                        - crest (str): Color representativo del equipo.
                        - players (list): Jugadores que conforman el equipo.
                        - points (int | float): Puntos acumulados por el equipo.
                    Retorna una lista vacía si el usuario no tiene equipos asociados.
                    Retorna None si ocurre una excepción durante la consulta.

        """

        try:
            print(usuario_id)
            equipos = await self.reposiroty_equipo.obtener_x_usuario_id(usuario_id)
            if equipos != None:
                print(equipos)
                lista_equipos = []
                for equipo in equipos:
                    
                    datos = {
                        'id': str(equipo['_id']),
                        'name': equipo['nombre_equipo'],
                        'crest': equipo['color'],
                        'players': equipo['jugadores_en_equipo'],
                        'points': equipo['puntos']

                    }
                    print()
                    lista_equipos.append(datos)
                return lista_equipos
            else:
                return []
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
            equipo = EquipoFantasy(id_usuario=body.get('id_usuario'),nombre_equipo=body.get('nombre_equipo'),color=body.get('color'))
            equipo_ingresado = await self.reposiroty_equipo.crear(equipo.to_dict())
            print('este equipo fue ingresado', equipo_ingresado)
            info = await self.repository_usuario.agregar_equipo(usuario_id=body.get('id_usuario'),equipo_info=equipo_ingresado)
            print("esta es la informacion: ", info)
            return equipo_ingresado
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
            #{'id': jugador_info.get('id'), 'precio': jugador_info.get('precio'), 'posicion':jugador_info.get('posicion'), 'nombre': jugador_info.get('nombre')}
            
            print(body)
            equipo_id = body.get('equipo_id')
            equipo = await self.reposiroty_equipo.obtener_por_id(equipo_id)
            
            jugador = await self.repository_jugador.obtener_por_id(int(body.get('jugador_id')))
            print(jugador)
            print(equipo)
            if int(equipo.get('presupuesto')) >= jugador.get('precio'):
                nuevo_presupuesto = int(equipo.get('presupuesto')) - int(jugador.get('precio'))
                objeto_jugador = {
                    'id': body.get('jugador_id'),
                    'precio': jugador.get('precio'),
                    'posicion': jugador.get('posicion'),
                    'nombre': jugador.get('nombre'),
                    'puntos': 0
                }
                datos ={
                    'presupuesto': nuevo_presupuesto
                }
                print(jugador)
                resultado = await self.reposiroty_equipo.agregar_jugador(equipo_id, objeto_jugador)
                resultado_actualizar = await self.reposiroty_equipo.actualizar(equipo_id,datos)
                print(resultado_actualizar)
                print(resultado)
                return resultado
            else:
                print('fondos insuficientes')
                raise ValueError("SALDO_INSUFICIENTE")
        except ValueError as e:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "code": "FONDOS_INSUFICIENTES",
                        "message": "No tiene fondos suficientes"
                    }
                    )
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
    
    async def eliminar_equipobyID(self, body: dict):
        try:
            usuario_id = body.get('usuario_id')
            equipo_id = body.get('equipo_id')
            response_equipo = await self.reposiroty_equipo.eliminar(equipo_id)
            await self.repository_usuario.eliminar_equipo(usuario_id=usuario_id, equipo_id=equipo_id)
            return response_equipo
        except Exception as e:
            print(e)
    async def eliminar_jugador_equipo(self, body: dict):
        try:
            
            jugador_id = body.get('jugador_id')
            equipo_id = body.get('equipo_id')
            equipo = await self.reposiroty_equipo.obtener_por_id(equipo_id)
            presupuesto = equipo.get('presupuesto')
            nuevo_presupuesto = 0
            for i in equipo.get('jugadores_en_equipo',[]):
                if i.get('id') == jugador_id:
                    nuevo_presupuesto = presupuesto + i.get('precio')
                else:
                    nuevo_presupuesto = presupuesto
            datos = {
                'presupuesto': nuevo_presupuesto
            }
            print(datos)
            actualizar_equipo = await self.reposiroty_equipo.actualizar(equipo_id=equipo_id,datos=datos)
            response_equipo = await self.reposiroty_equipo.eliminar_jugador_equipo(equipo_id=equipo_id,jugador_id=jugador_id)
            return response_equipo
        except Exception as e:
            print(e)

    async def obtener_jugadorPorRegex(self,nombre: str):
        """
    Busca jugadores cuyo nombre coincida parcialmente con el valor proporcionado,
    utilizando una búsqueda por expresión regular en el repositorio.

    Args:
        nombre (str): Texto (o patrón) a buscar dentro del nombre del jugador.

    Returns:
        list[dict]: Lista de diccionarios con los datos simplificados de cada
            jugador encontrado, con las siguientes claves:
                - id (str): Identificador del jugador (ObjectId convertido a str).
                - nombre (str): Nombre del jugador.
                - posicion (str): Posición del jugador.
                - precio (float | int): Precio del jugador.
                - equipo (str): Equipo al que pertenece el jugador.
            Retorna None si ocurre una excepción durante la consulta.

    """
        try:
            print(nombre)
            jugadores = []
            lista_jugadores = await self.repository_jugador.obtener_por_nombre_regex(nombre_jugador=nombre)
            print(lista_jugadores)
            
            for jugador in lista_jugadores:
                data = {
                    'id': str(jugador.get('_id')),
                    'nombre': jugador.get('nombre'),
                    'posicion' : jugador.get('posicion'),
                    'precio' : jugador.get('precio'),
                    'equipo': jugador.get('equipo')
                }
                jugadores.append(data)
            return jugadores
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

