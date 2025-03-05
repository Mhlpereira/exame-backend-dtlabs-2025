from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient
from app.api.services.auth_service import AuthService
from app.main import app
from app.api.models.user_model import UserModel
from app.api.services.user_service import UserService

client = TestClient(app)


@pytest.mark.asyncio
async def test_register_user():
    mock_user = UserModel(id="1", email="test@example.com", password="secret")
    with patch.object(
        UserService, "create_user", new_callable=AsyncMock, return_value=mock_user
    ):
        payload = {
            "email": "test@example.com",
            "password": "secret",
            "confirm_password": "secrete",
        }

        response = client.post("/auth/register", json=payload)

        assert response.status_code == 201
        assert response.json() == {
            "id": "1",
            "email": "test@example.com",
        }


@pytest.mark.asyncio
async def test_login():
    mock_token = "mock_access_token"
    with patch.object(
        AuthService, "login", new_callable=AsyncMock, return_value=mock_token
    ):
        payload = {
            "email": "test@example.com",
            "password": "minha_senha_secreta",
        }

        response = client.post("/auth/login", json=payload)

        assert response.status_code == 200
        assert response.json() == {
            "access_token": "mock_access_token",
            "token_type": "Bearer ",
        }


@pytest.mark.asyncio
async def test_login_logged_with_no_valid_user():
    with patch.object(
        AuthService,
        "login",
        new_callable=AsyncMock,
        side_effect=HTTPException(status_code=404, detail="User not found"),
    ):
        payload = {
            "email": "test@example.com",
            "password": "secret",
        }

        response = client.post("/auth/login", json=payload)

        assert response.status_code == 404
        assert response.json() == {
            "detail": "User not found",
        }
