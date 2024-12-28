# app/db/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(
                settings.MONGO_URI,
                maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
                minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
                serverSelectionTimeoutMS=settings.MONGODB_TIMEOUT_MS
            )
            self.db = self.client.banking_db
            print("Connected to MongoDB!")
        except Exception as e:
            print(f"Could not connect to MongoDB: {e}")

    async def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB!")

db = Database()