import motor.motor_asyncio

client = AsyncIOMotorClient("mongodb://mongo_admin:password@mongo:27017")

db = client.library
collection = db.books
