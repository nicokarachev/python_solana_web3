
from solana_lib import fetch_metadata
from mongo_lib import insert_token

mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # Example: Wrapped SOL

# Example usage
metadata = fetch_metadata(mint)
print(metadata)

insert_token(metadata)

while 1:
    print("Count:", count)
    count += 1