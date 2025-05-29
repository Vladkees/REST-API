
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient("mongodb://mongo_admin:password@mongo:27017")

db = client.library
collection = db.books
