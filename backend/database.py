from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client["contentcraft"]

users_collection = db["users"]
content_collection = db["content"]

print("✅ MongoDB Connected Successfully!")
