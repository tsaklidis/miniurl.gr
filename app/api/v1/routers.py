import logging
from fastapi import APIRouter, BackgroundTasks, Request

from app.core.config import settings
from app.core.rate_limit import rate_limit_response, limiter
from app.databases.general import resolve_url_from_dbs, DBActions, increase_click
from app.databases.redis import save_to_cache
from app.databases.serializers import UrlRequestRecord

from app.utils.generators import get_random_url_string
from app.errors.api_errors import NotFound


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/minify", responses=rate_limit_response)
@limiter.limit("30/minute")
async def minify_url(request: Request, item: UrlRequestRecord, background_tasks: BackgroundTasks):
    """
    Minify a provided url
    """
    actions = DBActions()
    if item.preferred_alias:
        exists = actions.get_url_by_alias(item.preferred_alias)
        if exists:
            raise ValueError(f"Alias '{item.preferred_alias}' already exists.")
    else:
        item.preferred_alias = get_random_url_string(6)

    item.url = f"{item.url}".rstrip('/').strip()

    # Save to cache/db in the background so we don't block the response
    background_tasks.add_task(save_to_cache, key=item.preferred_alias, value=item.url)

    background_tasks.add_task(actions.add_url, item.preferred_alias, item.url, item.description)
    base_url = settings.BASE_URL
    return {
        "minified_url": f"{base_url}/{item.preferred_alias}",
    }

@router.get("/{alias}")
async def resolve_url(alias: str, background_tasks: BackgroundTasks):
    """
    Resolve a minified url alias to its original url.
    No redirect, just return the original URL in JSON.
    """
    original_url = await resolve_url_from_dbs(alias)
    background_tasks.add_task(increase_click, alias)

    if not original_url:
        raise NotFound("Requested url not found")
    
    background_tasks.add_task(save_to_cache, alias, original_url)

    return {"url": original_url}
