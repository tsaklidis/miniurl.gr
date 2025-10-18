import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class EnvSettings(BaseSettings):
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

    # Redis (cache)
    REDIS_CACHE_HOST: str = os.getenv("REDIS_CACHE_HOST", "redis-cache")
    REDIS_CACHE_PORT: int = int(os.getenv("REDIS_CACHE_PORT", 6369))
    REDIS_CACHE_USE_SSL: bool = bool(int(os.getenv("REDIS_CACHE_USE_SSL", 0)))
    REDIS_CACHE_PASSWORD: str = os.getenv("REDIS_CACHE_PASSWORD", "")
    REDIS_CACHE_DB: int = int(os.getenv("REDIS_CACHE_DB", 0))
    REDIS_CACHE_URL: str = os.getenv("REDIS_CACHE_URL", f"redis://redis-cache:{REDIS_CACHE_PORT}/0")

    # Postgres
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "miniurl")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "miniurluser")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "strongpassword")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # CRITICAL = 50
    # FATAL = CRITICAL
    # ERROR = 40
    # WARNING = 30
    # INFO = 20
    # DEBUG = 10
    LOG_LEVEL : int = int(os.getenv("LOG_LEVEL", 30))
    SQL_LOG_LEVEL : int = int(os.getenv("SQL_LOG_LEVEL", 30))

    DB_NAME: str = os.getenv("DB_NAME", "miniurl.db")
    APP_API_TOKEN: str = os.getenv("APP_API_TOKEN", None)
    ADMIN_URL: str = os.getenv("ADMIN_URL", None)

settings = EnvSettings()
