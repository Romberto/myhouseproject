from fastapi import APIRouter


from .public import router as router_public
from .admin import router as router_admin
from .auth import router as router_auth
from ...config import settings

router = APIRouter(prefix=settings.api.v1.prefix)
# здесь записываются все роутеры v1
router.include_router(router_public)
router.include_router(router_admin)
router.include_router(router_auth)
