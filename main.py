import solana
from solana.rpc.api import Client
from solana.publickey import PublicKey

# Connect to mainnet
client = Client("https://api.mainnet-beta.solana.com")

# Token mint address (e.g., USDC)
mint_address = PublicKey("Es9vMFrzaCERU8D33Gdn5i2et2jTFoLQxkaFWwoTxkD9")

# Get token supply
response = client.get_token_supply(mint_address)
print("Total supply:", response["result"]["value"]["uiAmountString"])

