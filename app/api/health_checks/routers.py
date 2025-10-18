from fastapi import APIRouter, status, Request, Depends, HTTPException
from typing import Dict, Union

from fastapi.security import APIKeyHeader

from app.core.config import settings
from app.databases.redis import redis_cache
from app.core.rate_limit import limiter, rate_limit_response

router = APIRouter()
api_auth_scheme = APIKeyHeader(name='api-token', auto_error=True)


def internal_only(auth=Depends(api_auth_scheme)):
    if auth != settings.APP_API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return True

@router.get("/psql", responses=rate_limit_response)
def psql_status() -> Dict[str, bool]:
    return {"message": True}


@router.get("/redis", responses=rate_limit_response, dependencies=[Depends(internal_only)])
@limiter.limit("30/minute")
async def redis_health_check(request: Request) -> Dict[str, Union[bool, str]]:
    """
    Health check endpoint for Redis connectivity.

    Args:
        request (Request): The incoming FastAPI request object.

    Returns:
        dict: {"healthy": True} if Redis is reachable,
              {"healthy": False, "error": "..."} otherwise.

    Possible Responses:
        - 200: Redis health status
        - 429: Too Many Requests (rate limit exceeded)
    """
    try:
        await redis_cache.ping()
        return {"healthy": True}
    except Exception as e:
        return {"healthy": False, "error": str(e)}


@router.get("/redis_rw", responses=rate_limit_response, dependencies=[Depends(internal_only)])
@limiter.limit("10/minute")
async def redis_health_read_write_check(request: Request) -> Dict[str, Union[bool, str]]:
    """
    Health check endpoint for Redis read/write operations.

    Writes a temporary key-value pair, reads it back, and
    validates read/write functionality.

    Args:
        request (Request): The incoming FastAPI request object.

    Returns:
        dict: {"healthy": True} if read/write works,
              {"healthy": False, "error": "..."} otherwise.

    Possible Responses:
        - 200: Redis read/write health status
        - 429: Too Many Requests (rate limit exceeded)
    """
    try:
        test_key = "health:check"
        test_value = "ok"

        await redis_cache.set(test_key, test_value, ex=5)
        value = await redis_cache.get(test_key)

        return {"healthy": True} if value == test_value else {"healthy": False}
    except Exception as e:
        return {"healthy": False, "error": str(e)}

@router.get("/redis_data", responses=rate_limit_response, dependencies=[Depends(internal_only)])
async def list_all_redis_data():
    """
    Lists all key-value pairs in the Redis database.

    Returns:
        dict: Dictionary of {key: value} for all string keys.
    """
    data = {}
    async for key in redis_cache.scan_iter():
        value = await redis_cache.get(key)
        data[key] = value
    return data
