from .async_database import AsyncDatabaseConnection
import sys
import asyncio
from app.config import app_config


db_connection = AsyncDatabaseConnection(app_config.db_connection_url)
# if not asyncio.run(db_connection.test_connection()):
#     sys.exit(1)