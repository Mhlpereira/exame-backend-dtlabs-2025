from tortoise.models import Model
from tortoise import fields
import ulid


class UserModel(Model):
    id = fields.CharField(
        max_length=36, pk=True, unique=True, default=lambda: str(ulid.ulid())
    )
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255)

    class Meta:
        table = "users"
