import logging

from fastapi import APIRouter, BackgroundTasks, Request, Depends
from starlette.responses import RedirectResponse, Response

from app.api.v1.dependencies import get_valid_alias, get_db_actions
from app.core.rate_limit import rate_limit_response, limiter
from app.databases.general import DBActions
from app.databases.redis import save_to_cache

logger = logging.getLogger(__name__)


main_router = APIRouter(
    prefix="",
)

@main_router.get("/{alias}", responses=rate_limit_response)
@limiter.limit("60/minute")
async def resolve_url(
        request: Request,
        background_tasks: BackgroundTasks,
        original_url: str = Depends(get_valid_alias),
        db_actions: DBActions = Depends(get_db_actions)
):
    """
    Resolve a minified url alias to its original url
    """

    alias = request.path_params.get("alias")
    background_tasks.add_task(db_actions.increase_click, alias)
    background_tasks.add_task(save_to_cache, alias, original_url)

    return RedirectResponse(url=original_url, status_code=301)
