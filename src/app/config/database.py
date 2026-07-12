import motor.motor_asyncio
from .settings import settings


class MongoDBConnection:
    """Administra la conexión a MongoDB bajo el patrón de diseño Singleton.

    Garantiza que exista una única instancia de cliente y base de datos
    compartida por toda la aplicación, evitando abrir múltiples conexiones
    innecesarias.

    Attributes:
        client (AsyncIOMotorClient): Cliente asíncrono de conexión a MongoDB.
        db (AsyncIOMotorDatabase): Referencia a la base de datos en uso.
    """
    _instance = None

    def __new__(cls, uri=settings.MONGO_URI, db_name="Ftsy_mundial2026"):
        """Crea la instancia única de la conexión (Singleton).

        Si ya existe una instancia previa, la reutiliza en lugar de crear
        una nueva conexión a la base de datos.

        Args:
            uri (str): URI de conexión a MongoDB. Por defecto se toma de `settings`.
            db_name (str): Nombre de la base de datos a utilizar.

        Returns:
            MongoDBConnection: La única instancia existente de la clase.
        """
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            cls._instance.db = cls._instance.client[db_name]
        return cls._instance

    def get_db(self):
        """Obtiene la referencia a la base de datos activa.

        Returns:
            AsyncIOMotorDatabase: Objeto de base de datos para realizar operaciones.
        """
        return self.db
