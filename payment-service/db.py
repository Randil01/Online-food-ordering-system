from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URL)
db = client.get_database()

payments_collection = db["payments"]

# Access other services' collections (shared DB) check 
restaurants_collection = db["restaurants"]
orders_collection = db["orders"]