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
