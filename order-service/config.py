import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://FlaskApp:FlaskApp@flaskapp.wvwlvdx.mongodb.net/")
    PORT = int(os.getenv("PORT", 5002))
    DB_NAME = "Food_Ordering_System"
