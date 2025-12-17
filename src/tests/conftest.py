# Указываем backend
import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings
from src.core.models.base import Base
from src.crud.project import create_project, add_image_to_project
from src.shemas.projects import ProjectCreate, ImageCreate


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# Создаём engine и session_factory внутри фикстуры
@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        str(settings.db.test_url),
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


@pytest.fixture(scope="function")
async def project(session):
    project = await create_project(
        session,
        ProjectCreate(
            title="Slug test",
            slug="slug-test",
            shot_description="desc",
            quadrature=100,
        ),
    )
    return project


@pytest.fixture(scope="function")
async def images(session, project):
    image_data1 = ImageCreate(
        path_to_file="img1.jpg",
        public_url="http://img",
        is_preview=False,
        is_plan=False,
        is_gallery=True,
    )
    image_data2 = ImageCreate(
        path_to_file="img2.jpg",
        public_url="http://img",
        is_preview=False,
        is_plan=False,
        is_gallery=True,
    )
    img1 = await add_image_to_project(session, project.id, image_data1)
    img2 = await add_image_to_project(session, project.id, image_data2)

    return img1, img2
