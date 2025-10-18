import logging
from typing import Optional
from datetime import datetime, UTC
from sqlmodel import SQLModel, Field
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)

class Urls(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    alias: str = Field(unique=True, index=True)
    original_url: str
    description: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"server_default": func.now()}
    )
    total_clicks: int = Field(default=0)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    disabled: bool | None = None
    is_admin: bool | None = None
