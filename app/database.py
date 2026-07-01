from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.mongodb_url) #AsyncIOMotorClient is the async version of MongoClient, which allows for non-blocking database operations.
database = client[settings.database_name] # Get the database instance

# Collections (like tables in SQL)
users_collection = database.get_collection("users") 
transactions_collection = database.get_collection("transactions") 