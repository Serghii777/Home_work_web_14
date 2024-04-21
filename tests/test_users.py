from unittest.mock import patch

import pytest
from fastapi import UploadFile, HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.routes.users import router
from src.schemas.user import UserResponse

@pytest.fixture
async def app():
    app = FastAPI()
    app.include_router(router)
    yield app

@pytest.fixture
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def mock_user():
    return User(email="test@example.com", username="test_user")

@pytest.fixture
async def mock_db(mock_user):
    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add(mock_user)
        yield session

@pytest.mark.asyncio
async def test_get_current_user(async_client, mock_user):
    # Given
    headers = {"Authorization": "Bearer token"}
    # When
    response = await async_client.get("/users/me", headers=headers)
    # Then
    assert response.status_code == 200
    data = response.json()
    assert data == mock_user.dict()

@pytest.mark.asyncio
async def test_get_current_user_no_auth(async_client):
    # Given
    headers = {}
    # When
    response = await async_client.get("/users/me", headers=headers)
    # Then
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_not_found(async_client, mock_user):
    # Given
    headers = {"Authorization": "Bearer token"}
    with patch("src.routes.users.auth_service.get_current_user") as mock_get_user:
        mock_get_user.side_effect = HTTPException(status_code=404, detail="User not found")
        # When
        response = await async_client.get("/users/me", headers=headers)
        # Then
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_avatar(async_client, mock_db):
    # Given
    headers = {"Authorization": "Bearer token"}
    file = UploadFile(filename="avatar.jpg", content_type="image/jpeg")
    # When
    response = await async_client.patch("/users/avatar", headers=headers, files={"file": file})
    # Then
    assert response.status_code == 200
    data = response.json()
    assert data["avatar"] is not None