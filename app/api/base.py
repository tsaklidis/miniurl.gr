from fastapi import APIRouter
from app.api.v1 import routers as v1_endpoints
from app.api.health_checks import routers as health_check_endpoints

api_router = APIRouter(
    prefix="/api",
)

health_router = APIRouter(
    prefix="/health",
)

api_router.include_router(v1_endpoints.router, prefix="/v1.0", tags=["v1.0"])
health_router.include_router(health_check_endpoints.router,  tags=["health"])
