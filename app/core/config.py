import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс настройки.
    """

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_USERNAME: str

    BASE_URL: str = "http://127.0.0.1:8000"
    BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    STATIC_DIR: str = os.path.join(BASE_DIR, "static")

    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join('.env'))
    )

    @staticmethod
    def get_db_url():
        """
        Генерирует URL для подключения к PostgreSQL базе данных.

        :return: Строка с URL для подключения к базе данных.
        """
        return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
                f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

    @staticmethod
    def get_auth_data():
        """
        Возвращает данные для аутентификации, необходимые для работы с JWT.

        :return: Словарь с данными для аутентификации.
        """
        return {'secret_key': settings.SECRET_KEY, 'algorithm': settings.ALGORITHM}


settings = Settings()
