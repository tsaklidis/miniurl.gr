from fastapi import Depends
from sqlmodel import Session
from app.databases.manager import DatabaseManager
from app.databases.serializers import UrlRequestRecord
from app.errors.api_errors import NotFound
from app.databases.general import DBActions
from app.utils.generators import get_random_url_string


def get_session():
    session = DatabaseManager.get_session()
    try:
        yield session
    finally:
        session.close()

async def get_valid_alias(alias: str, session: Session = Depends(get_session)) -> str:
    actions = DBActions(session)
    original_url = actions.get_url_by_alias(alias)
    if not original_url:
        raise NotFound("Requested url not found")
    return original_url

async def get_valid_url_record(
        item: UrlRequestRecord,
        session: Session = Depends(get_session)
):
    actions = DBActions(session)
    if item.preferred_alias:
        exists = actions.get_url_by_alias(item.preferred_alias)
        if exists:
            raise ValueError(f"Alias '{item.preferred_alias}' already exists.")
    else:
        item.preferred_alias = get_random_url_string(6)

    item.url = f"{item.url}".rstrip('/').strip()
    return item

def get_db_actions(session: Session = Depends(get_session)):
    return DBActions(session)