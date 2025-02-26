from tortoise.models import Model
from tortoise import fields
import ulid

class UserModel(Model):
    id = fields.CharField(pk = True, unique = True, default = lambda: str(ulid.new()))
    email = fields.CharField(max_length = 20, unique = True)
    password = fields.CharField(max_length = 20)

    class Meta:
        table = "users"