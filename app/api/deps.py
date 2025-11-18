from typing import Generator
from sqlmodel import Session
from fastapi import Depends, BackgroundTasks
from app.errors.api_errors import NotFound
from app.databases.general import resolve_url_from_dbs, increase_click
from typing import Annotated
from app.databases.general import DBActionsHTTP

from app.databases.manager import DatabaseManager

def get_db() -> Generator[Session, None, None]:
   yield from DatabaseManager.get_session()

SessionDependency = Annotated[Session, Depends(get_db)]

def get_dbactions_http(session: SessionDependency) -> DBActionsHTTP:
   return DBActionsHTTP(session)

DBActionsHTTPDependency = Annotated[DBActionsHTTP, Depends(get_dbactions_http)]

async def get_valid_alias(alias: str) -> str:
    original_url = await resolve_url_from_dbs(alias)
    if not original_url:
        raise NotFound("Requested url not found")
    return alias

ValidAliasDependency = Annotated[str, Depends(get_valid_alias)]