import pytest
from unittest.mock import AsyncMock, patch
import bcrypt
from app.api.repositories.user_repository import UserRepository
from app.api.models.user_model import UserModel
from app.api.services.user_service import UserService


def test_hash_password():
    password = "minha_senha_secreta"
    hashed_password = UserService.hash_password(password)
    assert isinstance(hashed_password, str)
    assert bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def test_confirm_password():
    password = "minha_senha_secreta"
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    assert UserService.confirm_password(password, hashed_password) == True
    assert UserService.confirm_password("senha_errada", hashed_password) == False


@pytest.mark.asyncio
async def test_create_user_success():
    email = "test@example.com"
    password = "secret"

    mock_user = UserModel(
        id="1", email=email, password=UserService.hash_password(password)
    )
    with patch.object(
        UserRepository, "create_user", new_callable=AsyncMock, return_value=mock_user
    ):
        user = await UserService.create_user(email, password)
        assert user == mock_user


@pytest.mark.asyncio
async def test_create_user_password_error():
    email = "test@example.com"
    password = "minha_senha_secreta"

    with patch.object(UserService, "confirm_password", return_value=False):
        with pytest.raises(Exception) as exc_info:
            await UserService.create_user(email, password)
        assert str(exc_info.value) == "Error encrypting password"


@pytest.mark.asyncio
async def test_verify_password_success():
    email = "test@example.com"
    password = "minha_senha_secreta"
    hashed_password = UserService.hash_password(password)

    mock_user = UserModel(id="1", email=email, password=hashed_password)
    with patch.object(
        UserRepository,
        "get_user_by_email",
        new_callable=AsyncMock,
        return_value=mock_user,
    ):
        user = await UserService.verify_password(email, password)
        assert user == mock_user


@pytest.mark.asyncio
async def test_verify_password_failure():
    email = "test@example.com"
    password = "minha_senha_secreta"
    wrong_password = "senha_errada"

    mock_user = UserModel(
        id="1", email=email, password=UserService.hash_password(password)
    )
    with patch.object(
        UserRepository,
        "get_user_by_email",
        new_callable=AsyncMock,
        return_value=mock_user,
    ):
        with pytest.raises(Exception) as exc_info:
            await UserService.verify_password(email, wrong_password)
        assert str(exc_info.value) == "Email or password incorrect"


@pytest.mark.asyncio
async def test_get_user_by_id():
    user_id = "1"
    mock_user = UserModel(
        id=user_id, email="test@example.com", password="hashed_password"
    )

    with patch.object(
        UserRepository, "get_user_by_id", new_callable=AsyncMock, return_value=mock_user
    ):
        user = await UserService.get_user_by_id(user_id)
        assert user == mock_user
