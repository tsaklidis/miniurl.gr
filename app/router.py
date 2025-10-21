import logging

from fastapi import APIRouter, BackgroundTasks, Request
from starlette.responses import RedirectResponse, Response

from app.core.rate_limit import rate_limit_response, limiter
from app.databases.general import resolve_url_from_dbs, increase_click
from app.databases.redis import save_to_cache
from app.errors.api_errors import NotFound

logger = logging.getLogger(__name__)


main_router = APIRouter(
    prefix="",
)

@main_router.get("/{alias}", responses=rate_limit_response)
@limiter.limit("60/minute")
async def resolve_url(request: Request, alias: str, background_tasks: BackgroundTasks) -> Response:
    """
    Resolve a minified url alias to its original url
    """
    original_url, got_from_cache = await resolve_url_from_dbs(alias, got_from_cache=True)
    background_tasks.add_task(increase_click, alias)

    if not original_url:
        raise NotFound(detail="Requested url not found")

    if not got_from_cache:
        background_tasks.add_task(save_to_cache, alias, original_url)

    return RedirectResponse(url=original_url, status_code=301)
