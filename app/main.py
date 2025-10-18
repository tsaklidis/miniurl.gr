import os
import logging.config

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from sqladmin import Admin
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.admin.admin import UrlsAdmin, UserAdmin
from app.api import base as api_endpoints
from app.core.config import settings
from app.core.rate_limit import limiter
from app.databases.manager import DatabaseManager
from app.loggers import LOGGING_CONFIG
from app.router import main_router


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="miniurl.gr",
    description="A lightning-fast URL shortener.",
    version="1.0.0",
    contact={
        "name": "Stefanos I. Tsaklidis",
        "url": "https://tsaklidis.gr",
    }
)

# Add exception handler and limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.state.limiter = limiter

db_manager = DatabaseManager()
engine = db_manager.get_db_instance()
admin = Admin(
    app,
    engine,
    base_url=settings.ADMIN_URL,
)
admin.add_view(UrlsAdmin)
admin.add_view(UserAdmin)

# Register the catch-all router LAST
app.include_router(main_router)

# Register specific routers FIRST
app.include_router(api_endpoints.api_router)
app.include_router(api_endpoints.health_router)


# Serve static assets
app.mount("/static/js", StaticFiles(directory="front-end/static/js"), name="js")
app.mount("/static/css", StaticFiles(directory="front-end/static/css"), name="css")
app.mount("/static/img", StaticFiles(directory="front-end/static/img"), name="img")

# Serve index.html for root
@app.get("/")
def read_index():
    return FileResponse(os.path.join("front-end", "html", "index.html"))
