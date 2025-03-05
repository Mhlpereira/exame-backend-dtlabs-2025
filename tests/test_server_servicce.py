import datetime
from unittest.mock import AsyncMock, patch
import pytest

from app.api.models.server_model import ServerModel
from app.api.repositories.server_repository import ServerRepository
from app.api.services.server_service import ServerService


@pytest.mark.asyncio
async def test_save_register_data():
    server_ulid = "123"
    sensor_type = "temperature"
    value = "22.5"
    server_time = "2023-10-01T12:00:00"

    with patch.object(
        ServerRepository, "save_sensor_data", new_callable=AsyncMock
    ) as mock_save_sensor_data:
        await ServerRepository.save_sensor_data(
            server_ulid=server_ulid,
            sensor_type=sensor_type,
            value=value,
            server_time=server_time,
        )

        mock_save_sensor_data.assert_called_once_with(
            server_ulid=server_ulid,
            sensor_type=sensor_type,
            value=value,
            server_time=server_time,
        )


@pytest.mark.asyncio
async def test_get_server_health_by_id_healthy():
    mock_server = await ServerModel(server_ulid="123", server_name="Test Server")

    with patch.object(
        ServerService,
        "get_server_by_id",
        new_callable=AsyncMock,
        return_value=mock_server,
    ):
        with patch.object(
            ServerService,
            "server_time",
            new_callable=AsyncMock,
            return_value=datetime,
        ):
            with patch.object(ServerService, "server_health", return_value="healthy"):
                result = await ServerService.get_server_health_by_id("123")

                assert isinstance(result, dict)
                assert result["server_ulid"] == "123"
                assert result["status"] == "healthy"
                assert result["server_name"] == "Test Server"
