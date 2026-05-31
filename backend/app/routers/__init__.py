from app.routers.auth import router as auth_router
from app.routers.projects import router as projects_router
from app.routers.apis import router as apis_router, router_cases
from app.routers.scenes import router as scenes_router
from app.routers.reports import router as reports_router
from app.routers.run import router as run_router
from app.routers.mock import router as mock_router
from app.routers.import_export import router as import_export_router
from app.routers.dashboard import router as dashboard_router

__all__ = [
    "auth_router",
    "projects_router",
    "apis_router",
    "router_cases",
    "scenes_router",
    "reports_router",
    "run_router",
    "mock_router",
    "import_export_router",
    "dashboard_router",
]