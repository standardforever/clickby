import motor.motor_asyncio
from pymongo import DESCENDING, ASCENDING
from dateutil.parser import isoparse as IsoDateStringParser
from datetime import datetime

class AsyncDatabaseConnection():
    def __init__(self, mongodb_url, database_name = None):
        self.url = mongodb_url
        self.database_name = database_name
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.url)

        if self.database_name: self.db = self.client[self.database_name]
        else: self.db = None

    async def test_connection(self):
        try:
            databases =  await self.client.list_database_names()
            if not databases: return False
            return True
        except:
            return False

    async def get_many(self, database_name, collection_name, **kwargs):
        try:
            docs = await self.client[database_name][collection_name].find(kwargs).to_list(1000)
            return docs
        except:
            return None
    
    async def get_many_with_pipeline(self, database_name, collection_name, pipeline, **kwargs):
        try:
            total_docs = await self.client[database_name][collection_name].count_documents(kwargs)
            docs = await self.client[database_name][collection_name].aggregate(pipeline).to_list(None)
            return docs, total_docs

        except Exception as e:
            return None, 0

    async def get(self, database_name, collection_name, **kwargs):
        try:
            doc = await self.client[database_name][collection_name].find_one(kwargs)
            if doc: return doc
            else: return None
        except:
            return None

    async def create(self, database_name, collection_name, doc):
        doc["created_at"] = IsoDateStringParser(doc.pop("created_at"))
        doc["updated_at"] = IsoDateStringParser(doc.pop("updated_at"))
        try:
            insert_result = await self.client[database_name][collection_name].insert_one(doc)
            created_doc = await self.client[database_name][collection_name].find_one({"_id": insert_result.inserted_id})
            return created_doc
        except:
            return None

    async def update(self, database_name, collection_name, id, doc, **kwargs):
        try:
            doc.pop("_id", None)
            doc.pop("id", None)
            doc.pop("created_at", None)

            doc["updated_at"] = datetime.now()
            queries = {"id": id}
            if kwargs: queries.update(kwargs)

            update_result = await self.client[database_name][collection_name].update_one(queries, {"$set": doc})

            if update_result.modified_count == 1:
                updated_doc = await self.get(database_name, collection_name, id = id)
                return updated_doc

            else:
                return None
        except:
            return None

    async def delete(self, database_name, collection_name, **kwargs):
        try:
            delete_result = await self.client[database_name][collection_name].delete_one(kwargs)

            if delete_result.deleted_count == 1: return True

            return False
        except:
            return None

    async def create_index(self, database_name, collection_name, key, direction = DESCENDING, **kwargs):
        await self.client[database_name][collection_name].create_index([(key, direction)], **kwargs)

    async def is_collection_exist(self, database_name, collection_name):
        return collection_name in await self.client[database_name].list_collection_names()