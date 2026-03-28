from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URL)
db = client[Config.DB_NAME]

# Collection
restaurants_collection = db["restaurants"]