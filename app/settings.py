from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD']
    LOG_LEVEL: str

    DB_USER: str
    DB_USERPASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    TESTDB_USER: str
    TESTDB_USERPASS: str
    TESTDB_HOST: str
    TESTDB_PORT: int
    TESTDB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str

    SMTP_PASSWORD: str
    SMTP_USER: str
    SMTP_PORT: int
    SMTP_HOST: str

    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = '.env'


settings = Settings()
