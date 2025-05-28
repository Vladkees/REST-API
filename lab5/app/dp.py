import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo_admin:password@mongo:27017")
db = client.library
collection = db.books
