import pytest

from src.crud.project import (
    create_project,
    get_project_by_slug,
    update_project,
    delete_project,
    get_project,
)
from src.shemas.projects import ProjectCreate, ProjectUpdate


@pytest.mark.asyncio
async def test_create_project(session):
    data = ProjectCreate(
        title="Test house",
        slug="test-house12",
        shot_description="desc",
        quadrature=120,
        floors=2,
        bedrooms=3,
    )

    project = await create_project(session, data)

    assert project.id is not None
    assert project.slug == "test-house12"
    assert project.images == []


@pytest.mark.asyncio
async def test_get_project_by_slug(session):
    project = await create_project(
        session,
        ProjectCreate(
            title="Slug test",
            slug="slug-test",
            shot_description="desc",
            quadrature=100,
        ),
    )

    found = await get_project_by_slug(session, "slug-test")
    assert found.id == project.id


@pytest.mark.asyncio
async def test_update_project_partial(session):
    project = await create_project(
        session,
        ProjectCreate(
            title="Old",
            slug="old",
            shot_description="desc",
            quadrature=80,
        ),
    )

    updated = await update_project(
        session,
        project.id,
        ProjectUpdate(title="New"),
    )

    assert updated.title == "New"
    assert updated.slug == "old"


@pytest.mark.asyncio
async def test_delete_project_cascade_images(session):
    project = await create_project(
        session,
        ProjectCreate(
            title="Delete",
            slug="delete",
            shot_description="desc",
            quadrature=90,
        ),
    )

    assert await delete_project(session, project.id) is True
    assert await get_project(session, project.id) is None
