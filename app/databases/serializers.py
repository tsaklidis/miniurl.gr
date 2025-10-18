from pydantic import BaseModel, HttpUrl, constr
from typing import Optional

class UrlRequestRecord(BaseModel):
    url: HttpUrl
    preferred_alias: Optional[constr(min_length=5, max_length=20)] = None
    description: Optional[constr(max_length=255)] = None
