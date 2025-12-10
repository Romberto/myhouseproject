from fastapi import APIRouter


from .public_project import router as router_public
from .admin_project import router as router_admin
from .public_blog import router as router_public_blog
from .admin_blog import router as router_admin_blog
from .auth import router as router_auth
from ...config import settings

router = APIRouter(prefix=settings.api.v1.prefix)
# здесь записываются все роутеры v1
router.include_router(router_public)
router.include_router(router_admin)
router.include_router(router_public_blog)
router.include_router(router_admin_blog)
router.include_router(router_auth)
