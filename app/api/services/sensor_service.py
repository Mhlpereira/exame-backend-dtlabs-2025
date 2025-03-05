from datetime import datetime
from fastapi import HTTPException
from tortoise import Tortoise
from app.api.repositories.sensor_repository import SensorRepository


class SensorService:

    async def get_temperature() -> float:
        temperature = await SensorRepository.get_temperature()
        return temperature

    async def get_humidity() -> float:
        humidity = await SensorRepository.get_humidity()
        return humidity

    async def get_voltage() -> float:
        voltage = await SensorRepository.get_voltage()
        return voltage

    async def get_current() -> float:
        current = await SensorRepository.get_current()
        return current
