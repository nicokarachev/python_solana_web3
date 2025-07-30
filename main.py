
import os
import requests

from solana_lib import fetch_metadata
from mongo_lib import insert_token
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # Example: Wrapped SOL

# Example usage
metadata = fetch_metadata(mint)
print(metadata)

insert_token(metadata)


# return {
#         "name": safe_decode(data.name),
#         "symbol": safe_decode(data.symbol),
#         "uri": safe_decode(data.uri),
#         "seller_fee_basis_points": data.seller_fee_basis_points,
#     }
while 1:
    
    base_url = os.getenv("RAYDIUM_API")
    page_number = 1
    page_size = 1000
    return_size = page_size

    while return_size == page_size:

        api_url = f"{base_url}?poolType=all&poolSortField=liquidity&sortType=desc&page={page_number}&pageSize={page_size}"
        print(api_url)

        response = requests.get(api_url).json()    

        if response["success"] == False:
            continue
            
        page_number = page_number + 1

        for pool in response["data"]["data"]:

            insert_token({
                "address": pool["mintA"]["address"],
                "name": pool["mintA"]["name"],
                "symbol": pool["mintA"]["symbol"],
                "uri": pool["mintA"]["logoURI"],
                "seller_fee_basis_points": 0,
            })

            insert_token({
                "address": pool["mintB"]["address"],
                "name": pool["mintB"]["name"],
                "symbol": pool["mintB"]["symbol"],
                "uri": pool["mintB"]["logoURI"],
                "seller_fee_basis_points": 0,
            })

            


    # print(response.json())
    break