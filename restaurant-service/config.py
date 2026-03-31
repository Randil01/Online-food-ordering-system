import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL = os.getenv("MONGO_URL")
    PORT = int(os.getenv("PORT", 5001))
    DB_NAME = "Food_Ordering_System"