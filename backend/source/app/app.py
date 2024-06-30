from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import connection
from utils.init_database import load_data_users

from app.config import app_config

# Retrieve environment variables
environment = app_config.environment

app = FastAPI(
    root_path=f"/{environment}",
    docs_url=f"/api/v1/docs",
    openapi_url=f"/openapi.json"
)

@app.on_event("startup")
async def startup_events():
    await load_data_users()
    collection = await connection()
    app.collection = collection[0]
    app.collection_profit = collection[1]



app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_allowed,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

from router import api
from router import auth_route
from router import users_route

app.include_router(api.router,
                    prefix='/api/v1')

app.include_router(auth_route.router,
                prefix='/api/v1/auth')

app.include_router(users_route.router,
                prefix='/api/v1/user')

@app.get('/')
async def root():
    return {"Message": "Welcome to clickby Api with FastApi"}


