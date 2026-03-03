# Указываем backend
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi.testclient import TestClient

from src.config import settings
from src.core.models.base import Base
from src.core.models.db_helper import DataBaseHelper, db_helper
from src.crud.project import create_project, add_image_to_project
from src.main import main_app
from src.shemas.projects import ProjectCreate, ImageCreate
from src.api.api_v1.dependencies import require_admin


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# Создаём engine и session_factory внутри фикстуры
@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        # str(settings.db.test_url),
        "postgresql+asyncpg://general:testecret@localhost:5441/test_db",
        echo=False,
        poolclass=NullPool,  # ВАЖНО: без пула, чтобы избежать конфликтов loop'ов
        )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
async def async_auth_client(engine):
    async def override_require_admin():
        return {"user_id": 1}  # любой admin id

    async def override_db():
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        async with async_session() as session:
            yield session

    main_app.dependency_overrides[require_admin] = override_require_admin
    main_app.dependency_overrides[db_helper.session_getter] = override_db
    async with AsyncClient(
            transport=ASGITransport(app=main_app),
            base_url="http://127.0.0.1:8000/api/v1"
            ) as ac:
        yield ac


@pytest.fixture
async def async_not_auth_client():
    async with AsyncClient(
            transport=ASGITransport(app=main_app),
            base_url="http://127.0.0.1:8000/api/v1"
    ) as ac:
        yield ac
