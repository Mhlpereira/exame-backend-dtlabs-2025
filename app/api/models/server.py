from tortoise.models import Model
from tortoise import fields
import ulid


class ServerModel(Model):
    id = fields.CharField(pk = True, unique = True, default = lambda: str(ulid.new()))
    server_name = fields.CharField(max_length = 50)
    user = fields.ForeignKeyField("models.User", related_name="servers")

    class Meta:
        table = "servers"