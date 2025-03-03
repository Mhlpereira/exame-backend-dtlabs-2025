import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from tortoise import Tortoise

from app.api.repositories.server_repository import ServerRepository


@pytest.fixture
async def setup_database():
    await Tortoise.init(
        db_url="postgres://test:test@172.19.0.4:54323/test",
        modules={"models": ["app.api.models"]},
    )
    await Tortoise.generate_schemas()
    conn = Tortoise.get_connection("default")
    await conn.execute_query("TRUNCATE TABLE sensor_data CASCADE")

    yield

    await conn.execute_query("TRUNCATE TABLE sensor_data CASCADE")
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_save_sensor_data_successful(setup_database):
    server_ulid = "01FGZW7TRAEY9BSJKN5FQXJS7B"
    sensor_type = "temperature"
    value = 25.5
    server_time = "2023-01-01T12:00:00"

    with patch.object(
        Tortoise.get_connection("default"), "execute_query"
    ) as mock_execute:
        mock_execute.return_value = ([], 1)
        await ServerRepository.save_sensor_data(
            server_ulid, sensor_type, value, server_time
        )

        mock_execute.assert_called_once()
        args = mock_execute.call_args[0]
        assert "INSERT INTO sensor_data" in args[0]
        assert args[1][0] == server_ulid
        assert args[1][1] == sensor_type
        assert args[1][2] == value
        assert isinstance(args[1][3], datetime)


@pytest.mark.asyncio
async def test_save_sensor_data_no_connection():
    server_ulid = "01FGZW7TRAEY9BSJKN5FQXJS7B"
    sensor_type = "temperature"
    value = 25.5
    server_time = "2023-01-01T12:00:00"

    with patch.object(Tortoise, "get_connection", return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            await ServerRepository.save_sensor_data(
                server_ulid, sensor_type, value, server_time
            )

        assert exc_info.value.status_code == 500
        assert "Database connection not initialized" in exc_info.value.detail


@pytest.mark.asyncio
async def test_save_sensor_data_invalid_datetime():
    server_ulid = "01FGZW7TRAEY9BSJKN5FQXJS7B"
    sensor_type = "temperature"
    value = 25.5
    server_time = "formato-invalido"

    mock_connection = MagicMock()
    with patch.object(Tortoise, "get_connection", return_value=mock_connection):
        with pytest.raises(HTTPException) as exc_info:
            await ServerRepository.save_sensor_data(
                server_ulid, sensor_type, value, server_time
            )

        assert exc_info.value.status_code == 400
        assert "Error saving data" in exc_info.value.detail


@pytest.mark.asyncio
async def test_save_sensor_data_database_error(setup_database):
    server_ulid = "01FGZW7TRAEY9BSJKN5FQXJS7B"
    sensor_type = "temperature"
    value = 25.5
    server_time = "2023-01-01T12:00:00"

    with patch.object(
        Tortoise.get_connection("default"), "execute_query"
    ) as mock_execute:
        mock_execute.side_effect = Exception("Database error")

        with pytest.raises(HTTPException) as exc_info:
            await ServerRepository.save_sensor_data(
                server_ulid, sensor_type, value, server_time
            )

        assert exc_info.value.status_code == 400
        assert "Error saving data: Database error" in exc_info.value.detail


@pytest.mark.asyncio
async def test_save_sensor_data_parameter_validation():
    invalid_cases = [
        {
            "server_ulid": "",
            "sensor_type": "temperature",
            "value": 25.5,
            "server_time": "2023-01-01T12:00:00",
        },
        {
            "server_ulid": "01FGZW7TRAEY9BSJKN5FQXJS7B",
            "sensor_type": "temperature",
            "value": "not-a-number",
            "server_time": "2023-01-01T12:00:00",
        },
        {
            "server_ulid": "01FGZW7TRAEY9BSJKN5FQXJS7B",
            "sensor_type": "",
            "value": 25.5,
            "server_time": "2023-01-01T12:00:00",
        },
    ]

    mock_connection = MagicMock()
    with patch.object(Tortoise, "get_connection", return_value=mock_connection):
        for case in invalid_cases:
            with pytest.raises(HTTPException) as exc_info:
                await ServerRepository.save_sensor_data(**case)
            assert exc_info.value.status_code in [
                400,
                422,
            ]


@pytest.mark.parametrize(
    "sensor_type,value",
    [
        ("temperature", 25.5),
        ("humidity", 70.0),
        ("pressure", 1013.25),
        ("co2", 450),
    ],
)
@pytest.mark.asyncio
async def test_save_sensor_data_different_types(setup_database, sensor_type, value):
    server_ulid = "01FGZW7TRAEY9BSJKN5FQXJS7B"
    server_time = "2023-01-01T12:00:00"

    with patch.object(
        Tortoise.get_connection("default"), "execute_query"
    ) as mock_execute:
        mock_execute.return_value = ([], 1)

        await ServerRepository.save_sensor_data(
            server_ulid, sensor_type, value, server_time
        )

        mock_execute.assert_called_once()
        args = mock_execute.call_args[0]
        assert args[1][1] == sensor_type
        assert args[1][2] == value
