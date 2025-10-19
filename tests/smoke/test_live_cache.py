import pytest
import asyncio
import random
import string
import os

from app.databases.redis import save_to_cache, get_from_cache, redis_cache

def random_str(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@pytest.fixture(scope="session", autouse=True)
def set_redis_env():
    # Use env vars, default to localhost:6379 for CI
    os.environ.setdefault("REDIS_HOST", "localhost")
    os.environ.setdefault("REDIS_PORT", "6379")

@pytest.mark.asyncio
async def test_save_and_get_from_cache():
    key = f"testkey_{random_str()}"
    value = "testvalue"
    expire = 1  # seconds

    result = await save_to_cache(key, value, expire=expire)
    assert result is True or result is None

    cached_value = await get_from_cache(key)
    assert cached_value is not None
    assert cached_value.decode() == value if hasattr(cached_value, "decode") else cached_value == value

    await asyncio.sleep(expire + 1)
    expired = await get_from_cache(key)
    assert expired is None

@pytest.mark.asyncio
async def test_save_to_cache_no_expiration():
    key = f"testkey_{random_str()}"
    value = "persistent_value"

    await save_to_cache(key, value)
    cached_value = await get_from_cache(key)
    assert cached_value is not None
    assert cached_value.decode() == value if hasattr(cached_value, "decode") else cached_value == value

    await redis_cache.delete(key)

@pytest.mark.asyncio
async def test_save_to_cache_overwrites():
    key = f"testkey_{random_str()}"
    value1 = "value1"
    value2 = "value2"

    await save_to_cache(key, value1)
    cached_value1 = await get_from_cache(key)
    assert cached_value1.decode() == value1 if hasattr(cached_value1, "decode") else cached_value1 == value1

    await save_to_cache(key, value2)
    cached_value2 = await get_from_cache(key)
    assert cached_value2.decode() == value2 if hasattr(cached_value2, "decode") else cached_value2 == value2

    await redis_cache.delete(key)

@pytest.mark.asyncio
async def test_get_from_cache_missing_key():
    key = f"missing_{random_str()}"
    result = await get_from_cache(key)
    assert result is None