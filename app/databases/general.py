import logging
from typing import Union, Optional, Generator
from contextlib import contextmanager
from abc import ABC,abstractmethod

from pydantic import HttpUrl
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.databases.redis import get_from_cache
from app.databases.manager import DatabaseManager
from app.databases.models import Urls

logger = logging.getLogger(__name__)

class BaseDBActions(ABC):
    """
    Abstract base class for database actions related to URL shortening.
    
    Provides core methods for adding URLs, retrieving by alias, increasing click counts,
    and fetching the last inserted ID. Subclasses must provide a session context via
    `_get_session`.
    """
    @abstractmethod
    @contextmanager
    def _get_session(self) -> Generator[Session, None, None]:
        """
        Context manager to provide a database session.

        Must be implemented by subclasses.
        """
        ...
          
    def add_url(self, alias: str, original_url: Union[HttpUrl, str], description: str = None):
        urls_data = {
            "alias": alias,
            "original_url": original_url,
            "description": description
        }
        with self._get_session() as session:
            url_obj = Urls(**urls_data)
            session.add(url_obj)
            try:
                session.commit()
                return url_obj
            except IntegrityError as exc:
                session.rollback()
                # Check for unique constraint violation
                # TODO inspect if this can be done better
                if "unique" in str(exc).lower() or "duplicate" in str(exc).lower():
                    raise ValueError(f"Alias '{alias}' already exists.") from exc
                raise

    def get_url_by_alias(self, alias: str, return_object=False):
        """Get url based on alias"""
        with self._get_session() as session:
            statement = select(Urls).where(Urls.alias == alias)
            result = session.exec(statement).first()
            if return_object:
                return result
            return result.original_url if result else None

    async def increase_click(self, alias: str):
        with self._get_session() as session:
            statement = select(Urls).where(Urls.alias == alias)
            url_record = session.exec(statement).first()
            if not url_record:
                return None
            url_record.total_clicks = url_record.total_clicks + 1
            session.add(url_record)
            session.commit()
            logger.debug(f"Click count increased for alias: {alias} to {url_record.total_clicks}")
            return url_record.total_clicks

    def get_last_id(self) -> Optional[int]:
        """Get the last inserted ID in the Urls table"""
        with self._get_session() as session:
            statement = select(Urls).order_by(Urls.id.desc())
            result = session.exec(statement).first()
            return result.id if result else None
        


class DBActionsHTTP(BaseDBActions):
    """
    Database actions using a provided HTTP request session.

    Intended for use when the session is externally managed.
    """
    def __init__(self, session:Session):
        self.session = session

    @contextmanager
    def _get_session(self): 
        """Yield the provided session."""
        yield self.session


class DBActionsBackground(BaseDBActions):  
    """
    Database actions using a new session from the DatabaseManager.

    Intended for background tasks where the session is not externally managed.
    """  
    @contextmanager
    def _get_session(self): 
        """Create and yield a session for background operations."""
        engine = DatabaseManager.get_db_instance()
        with Session(engine) as session:
            yield session
        

async def resolve_url_from_dbs(alias: str, got_from_cache=False):
    """
    Resolve a minified url alias to its original url.
    First if it is available in cache, return that. If not, check the db.
    """

    from_cache = await get_from_cache(alias)
    if from_cache:
        # TODO: add metrics for cache hits/misses
        logger.debug("Hit cache for alias: %s", alias)
        original_url = from_cache
    else:
        # URL not found in cache, check the db
        actions = DBActionsBackground()
        original_url = actions.get_url_by_alias(alias=alias)

    if got_from_cache:
        return original_url, from_cache
    return original_url


async def increase_click(alias: str):
    """
    Increase click count for a given alias.
    """
    actions = DBActionsBackground()
    await actions.increase_click(alias)
