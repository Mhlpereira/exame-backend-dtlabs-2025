from unittest.mock import AsyncMock, patch
import pytest

from app.api.repositories.server_repository import ServerRepository


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
