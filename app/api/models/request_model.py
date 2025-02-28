from tortoise.models import Model
from tortoise import fields



class ServerTimeModel(Model):
    id = fields.IntField(pk=True)
    server= fields.ForeignKeyField("models.ServerModel", related_name="request_logs")
    timestamp = fields.FloatField()
    
    class Meta:
        table = "request_log"
        
    def __str__(self):
        return f"Log for server {self.server.name} in {self.timestamp}"