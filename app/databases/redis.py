import logging
import redis.asyncio as redis

from app.core.config import settings


logger = logging.getLogger(__name__)

# Cache Redis clients, based on environment settings
def setup_redis(url: str, port: int, db: int, use_ssl: bool = False, password: str = None):
    client = redis.Redis(
        host=url,
        port=port,
        db=db,
        decode_responses=True,
        ssl=use_ssl,
        password=password,
    )
    logger.info(f"Redis connected to: url:{url} port:{port}")
    return client

# Cache Redis (non-persistent)
redis_cache = setup_redis(
    url=settings.REDIS_CACHE_HOST,
    port=settings.REDIS_CACHE_PORT,
    db=settings.REDIS_CACHE_DB,
    use_ssl=settings.REDIS_CACHE_USE_SSL,
    password=settings.REDIS_CACHE_PASSWORD,
)


async def save_to_cache(key: str, value: str, expire: int = 86400):
    """
    Save a value to Redis cache.

    Args:
        key (str): The key under which the value will be stored.
        value (str): The value to store.
        expire (int, optional): Expiration time in seconds. If None, no expiration.
    """
    try:
        logger.info(f"Saving to cache: {key}:{value}")
        return await redis_cache.set(name=key, value=value, ex=expire)
    except Exception as e:
        logger.error(f"Failed to save to Redis: {e}")


async def get_from_cache(key):
    try:
        return await redis_cache.get(key)
    except Exception as e:
        logger.error(f"Failed to get from Redis: {e}")
        return None