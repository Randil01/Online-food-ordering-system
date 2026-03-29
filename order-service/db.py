from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URL)
db = client[Config.DB_NAME]

orders_collection = db["orders"]

# Access other services' collections if needed
restaurants_collection = db["restaurants"]
payments_collection = db["payments"]
