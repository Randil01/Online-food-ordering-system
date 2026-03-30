import certifi
from pymongo import MongoClient
from config import Config

ca = certifi.where()

client = MongoClient(Config.MONGO_URL, tlsCAFile=ca)
db = client[Config.DB_NAME]
deliveries_collection = db[Config.COLLECTION_NAME]
