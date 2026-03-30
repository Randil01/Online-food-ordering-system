import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    PORT = int(os.getenv("PORT", 5006))
    DB_NAME = "Food_Ordering_System"
    COLLECTION_NAME = "deliveries"
