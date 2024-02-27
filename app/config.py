from typing import Literal
from app import config
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO"]
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITM: str
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS: str
    REDIS_HOST: str
    REDIS_PORT: str
    

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
    
    
    @property
    def AUTH_DATA(self):
        return f"{self.SECRET_KEY}, {self.ALGORITM}"
    
    @property
    def CELERY_DATA(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    @property
    def REDIS_DATA(self):
        return f"redis://{self.REDIS_HOST}"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
