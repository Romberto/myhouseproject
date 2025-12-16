import pytest

from src.crud.project import add_image_to_project, create_project, image_is_preview, get_project
from src.shemas.projects import ImageCreate, ProjectCreate


@pytest.mark.asyncio
async def test_add_image(session, project):
    image_data = ImageCreate(
        path_to_file="img.jpg",
        public_url="http://img",
        is_preview=False,
        is_plan=False,
        is_gallery=True,
        )
    image = await add_image_to_project(
        session,
        project.id,
        image_data
    )

    assert image.project_id == project.id


@pytest.mark.asyncio
async def test_image_is_preview(session,project, images):

    img1, img2 = images

    refreshed = await get_project(session, project.id)

    assert len(refreshed.images) == 2

    # await image_is_preview(session, img2.id, project.id)
    # await image_is_preview(session, img1.id, project.id)
    #
    # refreshed = await get_project(session, project.id)
    #
    #
    # previews = [i for i in refreshed.images if i.is_preview]
    # assert len(previews) == 1
    # assert previews[1].id == img2.id
