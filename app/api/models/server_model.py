from tortoise.models import Model
from tortoise import fields


class ServerModel(Model):
    server_ulid = fields.CharField(max_length=36, pk = True, unique = True)
    server_name = fields.CharField(max_length = 100)
    user = fields.ForeignKeyField("models.UserModel", related_name="servers")
    
    
    class Meta:
        table = "servers"