from typing import ClassVar
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    SECRET_KEY: str = "teste"
    ALGORITHM: str = "HS256"
    DATABASE_URL: ClassVar[str] = "mysql+pymysql://root:root@mysql:3306/automacoes"

    class Config:
        env_file = ".env"

settings = Settings()
