from tortoise.models import Model
from tortoise import fields

class SensorModel(Model):

    id = fields.CharField(max_length=36, pk = True, unique = True)
    server_ulid = fields.ForeignKeyField("models.ServerModel", related_name="sensor_data")
    timestamp = fields.DatetimeField()
    temperature = fields.FloatField(null = True)
    humidity = fields.FloatField(null = True)
    voltage = fields.FloatField(null = True)
    current = fields.FloatField(null = True)

    class Meta:
        table = "sensor_data"