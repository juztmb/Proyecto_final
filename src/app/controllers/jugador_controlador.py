from ..repository import JugadorRepository
from ..models import jugador_factory

class JugadorControlador:
    """Controlador encargado de gestionar la lógica de negocio de los jugadores.

    Actúa como intermediario entre las rutas (API) y el repositorio de datos,
    utilizando el patrón Factory (`jugador_factory`) para instanciar el tipo
    de jugador correcto según su posición (Portero, Defensa, Medio, Delantero).

    Attributes:
        repository (JugadorRepository): Repositorio para el acceso a datos de jugadores.
    """
    def __init__(self):
        """Inicializa el controlador creando su propio repositorio de jugadores."""
        self.repository = JugadorRepository()


    async def crear(self, body:dict):
        """Crea un nuevo jugador a partir de los datos recibidos.

        Utiliza `jugador_factory` para construir el objeto jugador según su
        posición y luego lo persiste en la base de datos.

        Args:
            body (dict): Datos del jugador (nombre, equipo, posición, estadísticas, etc.).

        Returns:
            str | None: El id del jugador insertado, o None si ocurrió un error.
        """
        try:
            print(body)
            jugador = jugador_factory(body)
            print(jugador)
            return await self.repository.crear(jugador.to_dict())
        except Exception as e:
            print("error", e)
        
    async def obtener_por_id(self, id_jugador: str):
        """Busca un jugador por su identificador.

        Args:
            id_jugador (str): Identificador del jugador en la base de datos.

        Returns:
            Jugador | dict | None: Instancia del jugador reconstruida mediante
            el Factory, un diccionario vacío si no existe, o None si ocurre un error.
        """
        try:
            print(id_jugador)
            jugador = await self.repository.obtener_por_id(id_jugador)
            print(jugador)
            if jugador == {}:
                return jugador
            else:
                return jugador_factory(jugador)
        except Exception as e:
            print(e)
    
    async def obtener_todos(self):
        """Obtiene la lista completa de jugadores registrados.

        Returns:
            list[dict] | None: Lista de jugadores en formato diccionario.
        """
        try:
            return await self.repository.obtener_todos()
        except Exception as e:
            print(e)
    
    async def actualizar(self, body:dict):
        """Actualiza la información de un jugador existente.

        Args:
            body (dict): Debe incluir la clave "_id" con el identificador del
                jugador y el resto de campos a actualizar.

        Returns:
            int | None: Cantidad de documentos modificados.
        """
        try:
            id_jugador = body["_id"]
            del body["_id"]
            return await self.repository.actualizar(id_jugador,body)
        except Exception as e:
            print(e)
    
    async def eliminar(self, id_jugador: str):
        """Elimina un jugador de la base de datos.

        Args:
            id_jugador (str): Identificador del jugador a eliminar.

        Returns:
            int | None: Cantidad de documentos eliminados.
        """
        try:
            return await self.repository.eliminar(id_jugador)
        except Exception as e:
            print(e)

