from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from ..logging import LOGGER
import pymongo.errors  # Import the necessary pymongo errors

LOGGER(__name__).info("Connecting to your Mongo Database...")

try:
    # Initialize the async MongoDB client
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    mongodb = _mongo_async_.Music  # Access the 'Music' database

    # Check connection by pinging the database (optional, but a good practice)
    _mongo_async_.admin.command('ping')
    
    LOGGER(__name__).info("Successfully connected to your Mongo Database.")
except pymongo.errors.ConnectionError as e:
    LOGGER(__name__).error(f"Failed to connect to your Mongo Database: {e}")
    exit(1)  # Exit with a non-zero status to indicate failure
except Exception as e:
    # Catch any other unexpected errors
    LOGGER(__name__).error(f"Unexpected error: {e}")
    exit(1)
