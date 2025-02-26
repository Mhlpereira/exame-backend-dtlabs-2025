from tortoise.models import Model
from tortoise import fields
import ulid

class SensorModel(Model):

    id = fields.CharField(pk = True, unique = True, default = lambda: str(ulid.new()))
    server_ulid = fields.ForeignKeyField("models.Server", related_name="sensor_data")
    timestamp = fields.DatetimeField()
    temperature = fields.FloatField(null = True)
    humidity = fields.FloatField(null = True)
    voltage = fields.FloatField(null = True)
    current = fields.FloatField(null = True)

    class Meta:
        table = "sensor_data"