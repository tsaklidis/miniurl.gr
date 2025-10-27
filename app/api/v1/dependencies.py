from fastapi import Depends
from sqlmodel import Session
from app.databases.manager import DatabaseManager
from app.errors.api_errors import NotFound
from app.databases.general import DBActions

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

def get_db_actions(session: Session = Depends(get_session)):
    return DBActions(session)