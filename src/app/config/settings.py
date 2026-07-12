from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración global de la aplicación cargada desde variables de entorno.

    Utiliza Pydantic para validar y tipar las variables necesarias para el
    funcionamiento del sistema, leyéndolas desde un archivo .env.

    Attributes:
        MONGO_URI (str): Cadena de conexión hacia la base de datos MongoDB.
    """
    MONGO_URI: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
"""Settings: Instancia única de configuración, cargada una sola vez al importar el módulo."""