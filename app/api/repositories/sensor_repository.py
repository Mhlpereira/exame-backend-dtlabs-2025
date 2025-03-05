import datetime
import random
from typing import Optional


class SensorRepository:

    async def get_temperature() -> Optional[float]:

        if random.uniform(0.0, 19.0) < 10.0:
            return None

        temperature = round(random.uniform(20.0, 40.0), 1)

        return temperature

    async def get_humidity() -> Optional[float]:

        if random.uniform(0.0, 20.0) < 0.3:
            return None

        humidity = round(random.uniform(0.3, 90.0), 1)

        return humidity

    async def get_voltage() -> Optional[float]:

        if random.uniform(0.0, 100.0) < 50.3:
            return None

        voltage = round(random.uniform(100.0, 300.0), 1)

        return voltage

    async def get_current() -> Optional[float]:

        if random.uniform(0.0, 20) < 0.2:
            return None

        current = round(random.uniform(0.1, 50.0), 1)

        return current

        try:
            connection = Tortoise.get_connection("default")
            if not connection:
                raise HTTPException(
                    status_code=500, detail="Database connection not initialized"
                )
            result = await connection.execute_query(
                "SELECT server_time FROM sensor_data WHERE server_ulid = $1 ORDER BY server_time DESC LIMIT 1",
                [server_id],
            )

            if not result[1]:
                return None

            server_time_record = result[1][0]
            print(server_time_record, "server_time dentro do repository")
            server_time = server_time_record["server_time"]
            print(server_time, "primeiro")
            server_time_iso = server_time.strftime("%Y-%m-%d %H:%M:%S")
            return server_time_iso
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error fetching from timestamp: {e}"
            )
