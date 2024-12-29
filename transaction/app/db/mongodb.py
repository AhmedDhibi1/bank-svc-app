import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read MONGO_URI from environment
MONGO_URI = os.getenv("MONGO_URI")

# Initialize MongoDB client
client = MongoClient(MONGO_URI)

# Get the default database specified in the URI
db = client.get_database()

# Access a collection
transactions_collection = db["transactions"]
