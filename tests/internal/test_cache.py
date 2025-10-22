import pytest
from unittest.mock import AsyncMock, patch
import random
import string

from app.databases.redis import save_to_cache, get_from_cache


def random_str(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@pytest.mark.asyncio
async def test_save_and_get_from_cache():
    key = f"testkey_{random_str()}"
    value = "testvalue"
    expire = 1

    with patch("app.databases.redis.redis_cache", autospec=True) as mock_cache:
        # First get() → None (cache miss), second get() → cached value
        mock_cache.get = AsyncMock(side_effect=[None, value.encode()])
        mock_cache.set = AsyncMock(return_value=True)

        result = await save_to_cache(key, value, expire=expire)
        assert result is True

        cached_value = await get_from_cache(key)
        assert cached_value.decode() == value

        mock_cache.set.assert_awaited_once_with(name=key, value=value, ex=expire)
        assert mock_cache.get.await_count == 2  # called twice (miss + hit)


@pytest.mark.asyncio
async def test_save_to_cache_no_expiration():
    key = f"testkey_{random_str()}"
    value = "persistent_value"

    with patch("app.databases.redis.redis_cache", autospec=True) as mock_cache:
        mock_cache.set = AsyncMock(return_value=True)
        mock_cache.get = AsyncMock(return_value=value.encode())
        mock_cache.delete = AsyncMock(return_value=1)

        result = await save_to_cache(key, value)
        assert result is True

        cached_value = await get_from_cache(key)
        assert cached_value.decode() == value

        await mock_cache.delete(key)
        mock_cache.delete.assert_awaited_once_with(key)


@pytest.mark.asyncio
async def test_save_to_cache_prevents_overwrites():
    key = f"testkey_{random_str()}"
    value1 = "value1"
    value2 = "value2"

    with patch("app.databases.redis.redis_cache", autospec=True) as mock_cache:
        mock_cache.set = AsyncMock(return_value=True)
        # Always return the same value (cache already populated)
        mock_cache.get = AsyncMock(return_value=value1.encode())
        mock_cache.delete = AsyncMock(return_value=1)

        # First save: should succeed
        result1 = await save_to_cache(key, value1)
        assert result1 is True

        cached_value1 = await get_from_cache(key)
        assert cached_value1.decode() == value1

        # Second save: should NOT overwrite
        overwritten = await save_to_cache(key, value2)
        assert overwritten is False

        cached_value = await get_from_cache(key)
        assert cached_value.decode() == value1  # still old value

        await mock_cache.delete(key)
        mock_cache.delete.assert_awaited_once_with(key)


@pytest.mark.asyncio
async def test_get_from_cache_missing_key():
    key = f"missing_{random_str()}"
    with patch("app.databases.redis.redis_cache", autospec=True) as mock_cache:
        mock_cache.get = AsyncMock(return_value=None)

        result = await get_from_cache(key)
        assert result is None

        mock_cache.get.assert_awaited_once_with(key)
