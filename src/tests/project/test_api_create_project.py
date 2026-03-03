import pytest


@pytest.mark.parametrize(
    "data, status", [
        ({
            "title": "test title",
            "slug": "test slag1",
            "shot_description": "description",
            "description": "rfrgfaeff",
            "quadrature": 80,
            "floors": 1,
            "bedrooms": 1,
            "is_published": True
             }, 200),
({
            "title": "test title",
            "slug": "test slag1",
            "shot_description": "description",
            "description": "rfrgfaeff",
            "quadrature": 80,
            "floors": 1,
            "bedrooms": 1,
            "is_published": True
        }, 409),
({
            "title": "test title",
            "slug": "test slag2",
            "shot_description": "description",
            "description": "rfrgfaeff",
            "quadrature": 80,
            "floors": 1,
            "bedrooms": 1,
            "is_published": False
        }, 200),
({
            "title": "test title",
            "slug": "test slag3",
            "shot_description": "description",
            "description": "rfrgfaeff",
            "quadrature": 80,
            "floors": 0,
            "bedrooms": 5,
            "is_published": False
        }, 500),
({
            "title": "test title",
            "slug": "test slag98",
            "shot_description": "description",
            "description": "rfrgfaeff",
            "quadrature": 80,
            "floors": 3,
            "bedrooms": -1,
            "is_published": False
        }, 500),
({
            "title": "test title",
            "slug": "test slag6"
        }, 200),
({
            "slug": "test slag7"
        }, 422),
({
            "title": "test title"
        }, 422),
    ]
)
@pytest.mark.asyncio
async def test_create_project(async_auth_client, session, data, status):
    response = await async_auth_client.post(url="/admin/projects", json=data)
    assert response.status_code == status
