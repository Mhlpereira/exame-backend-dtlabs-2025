from tortoise.models import Model
from tortoise import fields

class SensorModel(Model):

    id = fields.CharField(max_length=36, pk = True, unique = True)
    server_ulid = fields.ForeignKeyField("models.ServerModel", related_name="sensor_data")
    timestamp = fields.DatetimeField()
    sensor_type = fields.CharField(max_length=80)
    value = fields.FloatField()

    class Meta:
        table = "sensor_data"