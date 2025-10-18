import logging
from sqlmodel import create_engine, Session


from app.core.config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    _db_instance = None

    @classmethod
    def get_db_instance(cls):
        if cls._db_instance is None:
            cls._db_instance = cls._create_db_instance()
        return cls._db_instance

    @staticmethod
    def _create_db_instance():
        db_url = settings.DATABASE_URL

        # Create PostgreSQL engine
        _engine = create_engine(db_url, echo=False)

        return _engine

    @classmethod
    def get_session(cls):
        engine = cls.get_db_instance()
        return Session(engine)


