import pytest


@pytest.mark.parametrize(
    "data", [
        {
            "title": "test title",
            "slug": "test slag",
            "shot_description": "description",
            "quadrature": 80,
            "floors": 1,
            "bedrooms": 1,
        }
    ]
)
@pytest.mark.asyncio
async def test_create_valid_project(async_auth_client, session, data):
    response = await async_auth_client.post(url="/admin/project", json=data)
    assert response.status_code == 201
