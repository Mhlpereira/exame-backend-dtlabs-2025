from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "localhost",
                "port": 5432,
                "user": os.getenv("PG_USER"),
                "password": os.getenv("PG_PASSWORD"),
                "database": os.getenv("PG_DB"),
            },
            "pool": {
                "max_size": 200,
                "min_size": 1,
                "max_queries": 50000,
                "max_inactive_connection_lifetime": 300,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["app.api.models"],
            "default_connection": "default",
        },
    },
}
