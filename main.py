
from solana_lib import fetch_metadata
from pymongo import MongoClient


mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # Example: Wrapped SOL

mongo_client = MongoClient("mongodb://localhost:27017/")

# Example usage
metadata = fetch_metadata(mint)
print(metadata)

