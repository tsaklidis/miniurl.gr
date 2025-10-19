import pytest
import asyncio
import random
import string

from app.databases.redis import save_to_cache, get_from_cache, redis_cache

def random_str(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@pytest.mark.asyncio
async def test_save_and_get_from_cache():
    key = f"testkey_{random_str()}"
    value = "testvalue"
    expire = 1  # seconds

    # Save to cache
    result = await save_to_cache(key, value, expire=expire)
    assert result is True or result is None  # Redis might return True or OK

    # Get from cache
    cached_value = await get_from_cache(key)
    assert cached_value is not None
    assert cached_value.decode() == value if hasattr(cached_value, "decode") else cached_value == value

    # Wait for expiration
    await asyncio.sleep(expire + 1)
    expired = await get_from_cache(key)
    assert expired is None

@pytest.mark.asyncio
async def test_save_to_cache_no_expiration():
    key = f"testkey_{random_str()}"
    value = "persistent_value"

    # Save with default expiration
    await save_to_cache(key, value)
    cached_value = await get_from_cache(key)
    assert cached_value is not None
    assert cached_value.decode() == value if hasattr(cached_value, "decode") else cached_value == value

    # Delete manually for clean-up
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