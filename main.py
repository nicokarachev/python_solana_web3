import solana
from solana.rpc.api import Client
from solders.pubkey import Pubkey
import base64
from construct import *

# Metaplex Metadata Program ID (fixed)
METADATA_PROGRAM_ID = Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")
mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # Example: Wrapped SOL

MetadataLayout = Struct(
    "key" / Int8ul,
    "update_authority" / Bytes(32),
    "mint" / Bytes(32),
    "name_length" / Int32ul,
    "name" / Bytes(32),
    "symbol_length" / Int32ul,
    "symbol" / Bytes(10),
    "uri_length" / Int32ul,
    "uri" / Bytes(200),
    "seller_fee_basis_points" / Int16ul,
    "has_creator" / Flag,
)

def safe_decode(b: bytes) -> str:
    return b.partition(b'\x00')[0].decode("utf-8", errors="ignore")

def get_metadata_pda(mint_address: str):
    mint_pubkey = Pubkey.from_string(mint_address)
    seeds = [
        b"metadata",
        bytes(METADATA_PROGRAM_ID),
        bytes(mint_pubkey)
    ]
    return Pubkey.find_program_address(seeds, METADATA_PROGRAM_ID)[0]


def fetch_metadata(mint_address: str):
    client = Client("https://api.mainnet-beta.solana.com")
    metadata_pda = get_metadata_pda(mint_address)

    result = client.get_account_info(metadata_pda)

    print(result)

    if not result.value:
        raise Exception("Metadata not found")

    data_base64 = bytes(result.value.data)
    data = MetadataLayout.parse(data_base64)

    print(data)

    return {
        "name": safe_decode(data.name),
        "symbol": safe_decode(data.symbol),
        "uri": safe_decode(data.uri),
        "seller_fee_basis_points": data.seller_fee_basis_points,
    }

# Example usage
metadata = fetch_metadata(mint)
print(metadata)

