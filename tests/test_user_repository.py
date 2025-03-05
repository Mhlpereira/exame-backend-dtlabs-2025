from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
import pytest
from tortoise import Tortoise


from app.api.repositories.user_repository import UserRepository, UserModel


@pytest.fixture(scope="function")
async def init_db():
    """Inicializa e finaliza o banco de dados para testes."""
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.api.models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_create_user(init_db):
    email = "mario@mario.com"
    password = "secret"

    user = await UserRepository.create_user(email=email, hash_password=password)

    assert user is not None
    assert user.id is not None
    assert user.email == email
    assert user.password == password


@pytest.mark.asyncio
async def test_create_user_None_email(init_db):
    email = None
    password = "secret"

    with patch.object(
        UserRepository, "create_user", new_callable=AsyncMock
    ) as mock_create_user:
        mock_create_user.side_effect = HTTPException(
            status_code=400,
            detail=f"Error creating user:",
        )

    with pytest.raises(HTTPException) as e:
        await UserRepository.create_user(email=email, hash_password=password)

    assert e.value.status_code == 404
    assert e.value.detail == "Null or missing email"


@pytest.mark.asyncio
async def test_create_user_None_password(init_db):
    email = "mario@mario.com"
    password = None

    with pytest.raises(HTTPException) as e:
        await UserRepository.create_user(email=email, hash_password=password)

    assert e.value.status_code == 404
    assert e.value.detail == "Null or missing password"


@pytest.mark.asyncio
async def test_get_user_by_email(init_db):
    email = "mario@mario.com"

    mock_user = UserModel(id=1, email="mario@mario.com", password="hashed_password")

    with patch.object(
        UserRepository, "get_user_by_email", new_callable=AsyncMock
    ) as mock_get_user_by_email:
        mock_get_user_by_email.return_value = mock_user

        user = await UserRepository.get_user_by_email(email)
        assert user is not None
        assert user.id == "1"
        assert user.email == "mario@mario.com"
        assert user.password == "hashed_password"

    mock_get_user_by_email.assert_called_once_with(email)


@pytest.mark.asyncio
async def test_get_user_by_email_invalid(init_db):
    email = "mario2@mario.com"

    with patch.object(
        UserRepository, "get_user_by_email", new_callable=AsyncMock
    ) as mock_get_user_by_email:
        mock_get_user_by_email.side_effect = HTTPException(
            status_code=404,
            detail="User not found",
        )

        with pytest.raises(HTTPException) as e:
            await UserRepository.get_user_by_email(email)

        assert e.value.status_code == 404
        assert e.value.detail == "User not found"

    mock_get_user_by_email.assert_called_once_with(email)


@pytest.mark.asyncio
async def test_get_user_by_id(init_db):
    id = "1"

    mock_user = UserModel(id="1", email="mario@mario.com", password="hashed_password")

    with patch.object(
        UserRepository, "get_user_by_id", new_callable=AsyncMock
    ) as mock_get_user_by_id:
        mock_get_user_by_id.return_value = mock_user

        user = await UserRepository.get_user_by_id(id)

        assert user is not None
        assert user.id == "1"
        assert user.email == "mario@mario.com"
        assert user.password == "hashed_password"

    mock_get_user_by_id.assert_called_once_with(id)


@pytest.mark.asyncio
async def test_get_user_by_id_invalid(init_db):
    id = "2"

    with patch.object(
        UserRepository, "get_user_by_id", new_callable=AsyncMock
    ) as mock_get_user_by_id:
        mock_get_user_by_id.side_effect = HTTPException(
            status_code=404,
            detail="User not found",
        )

        with pytest.raises(HTTPException) as e:
            await UserRepository.get_user_by_id(id)

        assert e.value.status_code == 404
        assert e.value.detail == "User not found"

    mock_get_user_by_id.assert_called_once_with(id)
