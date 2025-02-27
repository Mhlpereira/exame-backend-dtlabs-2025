from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import os

from app.middleware import auth_middleware

app =  FastAPI()

app.middleware("http")(auth_middleware)

register_tortoise(
    app,
    db_url ="postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@embarcados:5432/{os.getenv('POSTGRES_DB')}",    
    modules={"models": ["app.models"]},  
    generate_schemas=True,
    add_exception_handlers=True, 
)