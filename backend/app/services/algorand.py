from algosdk.v2client import algod, indexer
from algosdk import transaction, encoding
from app.config import get_settings

settings = get_settings()

CONTRACT_IDS = {
    "MILESTONE_ESCROW": 755290899,
    "HUSTLE_SCORE": 755290900,
}

def get_algod_client() -> algod.AlgodClient:

    return algod.AlgodClient("", settings.algorand_algod_address)

def get_indexer_client() -> indexer.IndexerClient:

    return indexer.IndexerClient("", settings.algorand_indexer_address)

def verify_wallet_signature(address: str, message: str, signature: str) -> bool:

    try:
        message_bytes = message.encode("utf-8")
        signature_bytes = encoding.base64.b64decode(signature)
        public_key = encoding.decode_address(address)
        
        return encoding.verify_bytes(message_bytes, signature_bytes, public_key)
    except Exception:
        return False

def get_account_info(address: str) -> dict:

    client = get_algod_client()
    try:
        return client.account_info(address)
    except Exception as e:
        return {"error": str(e)}

def get_account_balance(address: str) -> int:

    info = get_account_info(address)
    return info.get("amount", 0)
