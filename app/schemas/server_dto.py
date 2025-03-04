from typing import Optional

from pydantic import BaseModel


class OutputRegisterDataDTO(BaseModel):
    server_ulid: str
    timestamp: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None


class PayloadDTO(BaseModel):
    server_ulid: str


class OutputCreateServerDTO(BaseModel):
    server_name: str


class CreateServerDTO(BaseModel):
    name: str


class ListServerDTO(BaseModel):
    name: str
    server_ulid: str


class OutputServerHealthDTO(BaseModel):
    server_ulid: str
    status: str
    server_name: str


class SensorDataDTO(BaseModel):
    server_time: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None


class ListGetSensorDataDTO(BaseModel):
    timestamp: str
    values: dict[str, str]
