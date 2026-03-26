from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URL)
db = client[Config.DB_NAME]
deliveries_collection = db[Config.COLLECTION_NAME]
