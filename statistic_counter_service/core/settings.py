import os

TRUE_VALUES = {'True', 'true', '1'}


class Settings:
    API_DESCRIPTION = "Statistic REST API"
    API_VERSION = "0.0.0"

    CORS_ALLOW_HEADERS: list[str] = ["*"]
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_ORIGINS: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
    ]

    DEBUG = os.getenv('DEBUG') in TRUE_VALUES
    SHOW_TRACEBACK = os.getenv('SHOW_TRACEBACK') in TRUE_VALUES
    DATE_FORMAT = '%Y-%m-%d'

    # database
    DATABASE_URL: str = (f"postgresql+asyncpg://"
                         f"{os.getenv('POSTGRES_USER')}:"
                         f"{os.getenv('POSTGRES_PASSWORD')}@"
                         f"{os.getenv('POSTGRES_HOST')}:"
                         f"{os.getenv('POSTGRES_PORT')}/"
                         f"{os.getenv('POSTGRES_DB')}")
    DB_ENGINE_POOL_PRE_PING: bool = True
    DB_ENGINE_POOL_RECYCLE: int = -1
    DB_ENGINE_POOL_SIZE: int = 5
    DB_ENGINE_MAX_OVERFLOW: int = 10
    DB_ENGINE_POOL_TIMEOUT: int = 30
    SQL_ENGINE_ECHO: bool = os.getenv('SQL_ENGINE_ECHO') in TRUE_VALUES
