import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "data, status_code", [
        ({"login": "admin", "password": "admin"}, 401),
        ({"login": "", "password": "admin"}, 401),
        ({"login": "admin", "password": ""}, 401),
        ({"login": "admin", "password": "superadmin"}, 200)
    ]
)
@pytest.mark.asyncio
async def test_login_with_password(async_not_auth_client: AsyncClient, data, status_code):
    response = await async_not_auth_client.post("/login/password", json=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "data", [
        {
            "shot_description": "description",
            "quadrature": 80,
            "floors": 1,
            "bedrooms": 1,
        }
    ]
)
@pytest.mark.asyncio
async def test_create_project_no_auth(async_not_auth_client: AsyncClient, data):
    response = await async_not_auth_client.post('/admin/projects', json=data)
    assert response.status_code == 401
