from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import connection



app = FastAPI()


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
app.include_router(api.router,
                    tags=['ClickByApi'],
                    prefix='/api/v1')

@app.get('/')
async def root():
    return {"Message": "Welcome to clickby Api with FastApi"}

