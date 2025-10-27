from app.errors.api_errors import NotFound
from app.databases.general import resolve_url_from_dbs, DBActions

async def get_valid_alias(alias: str) -> str:
    original_url = await resolve_url_from_dbs(alias)
    if not original_url:
        raise NotFound("Requested url not found")
    return original_url

def get_db_actions():
    return DBActions()
