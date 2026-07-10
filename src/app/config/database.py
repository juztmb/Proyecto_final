import motor.motor_asyncio
from .settings import settings


class MongoDBConnection:
    """
        Clase abstracta bajo el patron de singleton, que realiza la conexion a la base de datos.
    """
    _instance = None

    def __new__(cls, uri=settings.MONGO_URI, db_name="Ftsy_mundial2026"):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            cls._instance.db = cls._instance.client[db_name]
        return cls._instance

    def get_db(self):
        return self.db
