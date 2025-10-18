from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, enabled=True)

rate_limit_response = {
    429: {
        "description": "Too Many Requests - rate limit exceeded",
        "content": {
            "application/json": {
                "example": {"error": "Rate limit exceeded: 10 per 1 minute"}
            }
        },
    }
}