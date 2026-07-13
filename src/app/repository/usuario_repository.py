from bson import ObjectId
from ..config import conexion


class UsuarioRepository:
    """Repositorio encargado del acceso a datos de los usuarios en MongoDB.

    Encapsula las operaciones CRUD sobre la colección "usuarios"
    (clientes y administradores), desacoplando a los controladores del
    detalle de la base de datos (patrón Repository).

    Attributes:
        collection: Colección de MongoDB "usuarios".
    """
    def __init__(self):
        """Obtiene la conexión Singleton a la base de datos y la colección de usuarios."""
        self.collection = conexion.get_db()["usuarios"]

    async def crear(self, usuario: dict):
        """Inserta un nuevo usuario en la base de datos.

        Args:
            usuario (dict): Datos del usuario a insertar.

        Returns:
            str: Identificador del documento insertado.
        """
        result = await self.collection.insert_one(usuario)
        return str(result.inserted_id)

    async def obtener_por_id(self, usuario_id: str):
        """Busca un usuario por su identificador.

        Args:
            usuario_id (str): Identificador del usuario.

        Returns:
            dict | None: Documento del usuario encontrado, o None si no existe.
        """
        return await self.collection.find_one({"_id": ObjectId(usuario_id)})
    
    async def obtener_por_correo(self, correo: str):
        """Busca un usuario por su correo electrónico.

        Útil para procesos de inicio de sesión o validación de correo
        único al registrar un usuario.

        Args:
            correo (str): Correo electrónico del usuario.

        Returns:
            dict | None: Documento del usuario encontrado, o None si no existe.
        """
        print(correo)
        return await self.collection.find_one({"email": correo})
    
    async def obtener_todos(self):
        """Obtiene todos los usuarios registrados.

        Returns:
            list[dict]: Lista de documentos de usuarios.
        """
        cursor = self.collection.find({})
        return [doc async for doc in cursor]

    async def actualizar(self, usuario_id: str, datos: dict):
        """Actualiza los datos de un usuario existente.

        Args:
            usuario_id (str): Identificador del usuario a actualizar.
            datos (dict): Campos a actualizar.

        Returns:
            int: Cantidad de documentos modificados.
        """
        result = await self.collection.update_one(
            {"_id": ObjectId(usuario_id)},
            {"$set": datos}
        )
        return result.modified_count

    async def eliminar(self, usuario_id: str):
        """Elimina un usuario de la base de datos.

        Args:
            usuario_id (str): Identificador del usuario a eliminar.

        Returns:
            int: Cantidad de documentos eliminados.
        """
        result = await self.collection.delete_one({"_id": ObjectId(usuario_id)})
        return result.deleted_count