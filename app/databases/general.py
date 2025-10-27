import logging
from typing import Union

from pydantic import HttpUrl
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.databases.redis import get_from_cache
from app.databases.manager import DatabaseManager
from app.databases.models import Urls

logger = logging.getLogger(__name__)


class DBActions:
    def __init__(self, session: Session):
        self.session = session

    def add_url(self, alias: str, original_url: Union[HttpUrl, str], description: str = None):
        urls_data = {
            "alias": alias,
            "original_url": original_url,
            "description": description
        }
        url_obj = Urls(**urls_data)
        self.session.add(url_obj)
        try:
            self.session.commit()
            return url_obj
        except IntegrityError as exc:
            self.session.rollback()
            if "unique" in str(exc).lower() or "duplicate" in str(exc).lower():
                raise ValueError(f"Alias '{alias}' already exists.") from exc
            raise

    def get_url_by_alias(self, alias: str, return_object=False):
        statement = select(Urls).where(Urls.alias == alias)
        result = self.session.exec(statement).first()
        if return_object:
            return result
        return result.original_url if result else None

    def increase_click(self, alias: str):
        url_record = self.get_url_by_alias(alias, return_object=True)
        if url_record:
            url_record.total_clicks = url_record.total_clicks + 1
            self.session.add(url_record)
            self.session.commit()
            logger.debug(f"Click count increased for alias: {alias} to {url_record.total_clicks}")
            return url_record.total_clicks

    def get_last_id(self):
        statement = select(Urls).order_by(Urls.id.desc())
        result = self.session.exec(statement).first()
        return result.id if result else None


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
        actions = DBActions()
        original_url = actions.get_url_by_alias(alias=alias)

    if got_from_cache:
        return original_url, from_cache
    return original_url

async def increase_click(alias: str):
    """
    Increase click count for a given alias.
    """
    actions = DBActions()
    await actions.increase_click(alias)
