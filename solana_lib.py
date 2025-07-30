import os
from dotenv import load_dotenv
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from construct import *

# Load environment variables from .env file
load_dotenv()

# Metaplex Metadata Program ID (fixed)
METADATA_PROGRAM_ID = Pubkey.from_string(os.getenv("METADATA_PROGRAM_ID"))
solana_client = Client(os.getenv("SOLANA_RPC"))

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
    metadata_pda = get_metadata_pda(mint_address)
    result = solana_client.get_account_info(metadata_pda)

    if not result.value:
        raise Exception("Metadata not found")

    data_base64 = bytes(result.value.data)
    data = MetadataLayout.parse(data_base64)

    return {
        "name": safe_decode(data.name),
        "symbol": safe_decode(data.symbol),
        "uri": safe_decode(data.uri),
        "seller_fee_basis_points": data.seller_fee_basis_points,
    }

