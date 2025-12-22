import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import sys

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "mental_health_db") # Default to "mental_health_db" if not set

class Database:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        """
        Establishes an asynchronous connection to the MongoDB database.
        """
        print("Connecting to MongoDB...")
        if not MONGO_URI:
            print("Error: MONGO_URI environment variable is not set.", file=sys.stderr)
            sys.exit(1)
        
        try:
            self.client = AsyncIOMotorClient(MONGO_URI)
            # The ismaster command is cheap and does not require auth.
            await self.client.admin.command('ismaster')
            self.db = self.client[DB_NAME]
            print(f"Successfully connected to MongoDB database: {DB_NAME}")
        except ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}", file=sys.stderr)
            sys.exit(1)

    async def close(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

# Create a single instance of the Database
db_manager = Database()

async def get_database():
    if db_manager.db is None:
        await db_manager.connect()
    return db_manager.db
