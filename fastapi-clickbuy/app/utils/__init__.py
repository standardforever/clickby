from app.utils.database import database_live_connect, database_local_connect
import asyncio

# collection = database_live_connect()
collection = database_local_connect()

