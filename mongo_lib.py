import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

mongo_client = MongoClient(os.getenv("MONGO_URI"))

db = mongo_client[os.getenv("solana_python")]
collection = db["token"]

def insert_token(token):
    old_token = collection.find_one(token)

    if old_token :
        return
    
    collection.insert_one(token)
