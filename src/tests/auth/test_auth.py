import pytest
from httpx import AsyncClient

from src.api.api_v1.auth import login_with_password

@pytest.mark.parametrize(
    "data, status_code", [
        ({"login":"admin","password":"admin"}, 401),
        ({"login":"","password":"admin"}, 401),
        ({"login":"admin","password":""}, 401),
        ({"login":"admin","password":"superadmin"},200)
    ]
)
@pytest.mark.asyncio
async def test_login_with_password(async_client: AsyncClient, data, status_code):
    response = await async_client.post("/api/v1/login/password", json=data)
    assert response.status_code == status_code