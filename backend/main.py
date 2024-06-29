from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import connection

from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()


# Retrieve environment variables
environment = quote_plus(os.getenv("environment"))

app = FastAPI(
    root_path=f"/{environment}",
    docs_url=f"/api/v1/docs",
    openapi_url=f"/openapi.json"
)

@app.on_event("startup")
async def startup_events():
    collection = await connection()
    app.collection = collection[0]
    app.collection_profit = collection[1]


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

from app.router import api
from app.router import sort
app.include_router(api.router,
                    # tags=['ClickByApi'],
                    prefix='/api/v1')

app.include_router(sort.router,
                prefix='/api/v1/sort')

@app.get('/')
async def root():
    return {"Message": "Welcome to clickby Api with FastApi"}

