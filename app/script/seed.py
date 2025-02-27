import asyncio
from tortoise import Tortoise
from app.api.models.server_model import ServerModel
from app.api.models.user_model import UserModel
import os

async def seed():
    
    await Tortoise.init(
        db_url=f"postgres://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@localhost:5432/{os.getenv('PG_DB')}",
        modules={"models": ["app.api.models"]},
    )
    await Tortoise.generate_schemas()

    user1 = await UserModel.create(id='01JN4GYD78FFMAKMER7CX3BJ09', email='mario@example.com' , password='secret')
    user2 = await UserModel.create(id='01JN4GYMF31MQJ66X6Y9TJY28R', email='maria@example.com', password='secret2')

    print(f"User created: {user1.email}, {user2.email}")

    server1 = await ServerModel.create(id='01JN4HCDW7ZF0TFMXWKRFV06GG', server_name="Dolly #1" , user=user1)
    server2 = await ServerModel.create(id='01JN4HCMRV5GK5VRWR5P5KN1TC', server_name="Dolly #2", user=user2)
    
    print(f"Server created: {server1.server_name}, {server2.server_name}")
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(seed())
