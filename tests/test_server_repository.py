from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
import pytest
from tortoise import Tortoise


from app.api.repositories.server_repository import (
    ServerRepository,
    ServerModel,
    UserModel,
)


@pytest.fixture(scope="function")
async def init_db():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.api.models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_get_create_server(init_db):
    mock_user = await UserModel.create(
        id="1", email="mario@mario.com", password="secret"
    )

    name = "server"
    user = mock_user

    with patch("ulid.new", return_value="1"):
        mock_server = await ServerModel.create(
            server_ulid="1", server_name=name, user=user
        )

        with patch.object(
            ServerModel, "create", new_callable=AsyncMock, return_value=mock_server
        ) as mock_create:
            server = await ServerRepository.create_server(name=name, user=user)

    assert server is not None
    assert isinstance(server, ServerModel)
    assert server.server_ulid == "1"
    assert server.server_name == "server"
    assert server.user == mock_user


@pytest.mark.asyncio
async def test_get_create_server_with_no_user(init_db):

    name = "server"
    user = None

    with patch.object(
        ServerRepository, "create_server", new_callable=AsyncMock
    ) as mock_create_server:
        mock_create_server.side_effect = HTTPException(
            status_code=404,
            detail="You must be logged in to create a server",
        )

        with pytest.raises(HTTPException) as e:
            await ServerRepository.create_server(name=name, user=user)

    assert e.value.status_code == 404
    assert e.value.detail == "You must be logged in to create a server"
    mock_create_server.assert_called_once_with(name=name, user=user)


@pytest.mark.asyncio
async def test_save_sensor_data(init_db):
    mock_sensor = {
        "server_ulid": "1",
        "sensor_type": "humidity",
        "value": 10.0,
        "server_time": "2025-03-04T19:52:17.652282",
    }

    with patch.object(
        ServerRepository, "save_sensor_data", new_callable=AsyncMock
    ) as mock_save_sensor_data:
        mock_save_sensor_data.return_value = mock_sensor

        sensor = await ServerRepository.save_sensor_data(mock_sensor)

    assert sensor is not None
    assert sensor["server_ulid"] == "1"
    assert sensor["sensor_type"] == "humidity"
    assert sensor["value"] == 10.0
    assert sensor["server_time"] == "2025-03-04T19:52:17.652282"

    mock_save_sensor_data.assert_called_once_with(mock_sensor)


@pytest.mark.asyncio
async def test_save_sensor_data_no_db_connection():
    mock_sensor = {
        "server_ulid": "1",
        "sensor_type": "humidity",
        "value": 10.0,
        "server_time": "2025-03-04T19:52:17.652282",
    }

    with patch.object(
        ServerRepository, "save_sensor_data", new_callable=AsyncMock
    ) as mock_save_sensor_data:
        mock_save_sensor_data.side_effect = HTTPException(
            status_code=500,
            detail="Database connection not initialized",
        )
        with patch.object(Tortoise, "get_connection", return_value=None):
            with pytest.raises(HTTPException) as e:
                await ServerRepository.save_sensor_data(
                    server_ulid=mock_sensor["server_ulid"],
                    sensor_type=mock_sensor["sensor_type"],
                    value=mock_sensor["value"],
                    server_time=mock_sensor["server_time"],
                )

    assert e.value.status_code == 500
    assert e.value.detail == "Database connection not initialized"

    mock_save_sensor_data.assert_called_once_with(
        server_ulid=mock_sensor["server_ulid"],
        sensor_type=mock_sensor["sensor_type"],
        value=mock_sensor["value"],
        server_time=mock_sensor["server_time"],
    )


@pytest.mark.asyncio
async def test_save_sensor_data_bad_request(init_db):
    mock_sensor = {
        "server_ulid": "1",
        "sensor_type": "humidity",
        "value": 10.0,
        "server_time": "2025-03-04T19:52:17.652282",
    }

    with patch.object(
        ServerRepository, "save_sensor_data", new_callable=AsyncMock
    ) as mock_save_sensor_data:
        mock_save_sensor_data.side_effect = HTTPException(
            status_code=400,
            detail="Error saving data:",
        )
        with patch.object(Tortoise, "get_connection", return_value=None):
            with pytest.raises(HTTPException) as e:
                await ServerRepository.save_sensor_data(
                    server_ulid=mock_sensor["server_ulid"],
                    sensor_type=mock_sensor["sensor_type"],
                    value=mock_sensor["value"],
                    server_time=mock_sensor["server_time"],
                )

    assert e.value.status_code == 400
    assert e.value.detail == "Error saving data:"

    mock_save_sensor_data.assert_called_once_with(
        server_ulid=mock_sensor["server_ulid"],
        sensor_type=mock_sensor["sensor_type"],
        value=mock_sensor["value"],
        server_time=mock_sensor["server_time"],
    )


@pytest.mark.asyncio
async def test_get_server_by_id(init_db):
    mock_user = await UserModel.create(
        id="1", email="mario@mario.com", password="secret"
    )
    mock_server = await ServerModel.create(
        server_ulid="1", server_name="teste", user=mock_user
    )

    with patch.object(
        ServerRepository, "get_server_by_id", new_callable=AsyncMock
    ) as mock_get_server_by_id:
        mock_get_server_by_id.return_value = mock_server

        server = await ServerRepository.get_server_by_id(server_ulid="1")

    assert server is not None
    assert server.server_ulid == "1"
    assert server.server_name == "teste"
    assert isinstance(server.user, UserModel)
    assert isinstance(server, ServerModel)

    mock_get_server_by_id.assert_called_once_with(server_ulid="1")


@pytest.mark.asyncio
async def test_get_server_by_id_with_404(init_db):
    mock_user = await UserModel.create(
        id="1", email="mario@mario.com", password="secret"
    )
    mock_server = await ServerModel.create(
        server_ulid="1", server_name="teste", user=mock_user
    )

    with patch.object(
        ServerRepository, "get_server_by_id", new_callable=AsyncMock
    ) as mock_get_server_by_id:
        mock_get_server_by_id.side_effect = HTTPException(
            status_code=404, detail="Server not found"
        )
        with pytest.raises(HTTPException) as e:
            await ServerRepository.get_server_by_id(server_ulid="4")

    assert e.value.status_code == 404
    assert e.value.detail == "Server not found"
    mock_get_server_by_id.assert_called_once_with(server_ulid="4")
