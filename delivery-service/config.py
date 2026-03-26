import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    PORT = int(os.getenv("PORT", 5005))
    DB_NAME = "delivery_db"
    COLLECTION_NAME = "deliveries"
