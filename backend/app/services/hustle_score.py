"""
HustleScore Service - Backend interaction with Algorand HustleScore contract
"""
import os
from algosdk import mnemonic, account
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCallTxn, OnComplete
from algosdk.abi import ABIType
from algosdk.encoding import decode_address
import base64

# Contract configuration
HUSTLE_SCORE_APP_ID = int(os.getenv('HUSTLE_SCORE_APP_ID', '755290900'))
ALGOD_SERVER = os.getenv('ALGOD_SERVER', 'https://testnet-api.algonode.cloud')
ALGOD_TOKEN = os.getenv('ALGOD_TOKEN', '')

# Admin wallet (signs reputation transactions)
ADMIN_MNEMONIC = os.getenv('ADMIN_WALLET_MNEMONIC', '')


def get_algod_client():
    """Get Algod client for TestNet."""
    return algod.AlgodClient(ALGOD_TOKEN, ALGOD_SERVER)


def get_admin_account():
    """Get admin account from mnemonic."""
    if not ADMIN_MNEMONIC:
        raise ValueError("ADMIN_WALLET_MNEMONIC not configured in .env")
    
    private_key = mnemonic.to_private_key(ADMIN_MNEMONIC)
    address = account.address_from_private_key(private_key)
    return address, private_key


async def ensure_student_initialized(student_address: str) -> bool:
    """
    Check if student has box storage initialized. If not, initialize it.
    Returns True if already initialized, False if newly created.
    """
    try:
        # Check if student already has a score
        score = await get_student_score(student_address)
        return True  # Already initialized
    except:
        # Not initialized, mint initial SBT
        try:
            await mint_initial_score(student_address)
            return False  # Newly initialized
        except Exception as e:
            print(f"Error initializing student: {e}")
            raise


async def mint_initial_score(student_address: str):
    """Initialize a brand new student with 0 score (creates box)."""
    client = get_algod_client()
    admin_address, admin_private_key = get_admin_account()
    
    # Get suggested params
    params = client.suggested_params()
    
    # Prepare method call arguments
    # Method signature: mint_initial(account)student
    method_selector = bytes.fromhex("762ce8fb")  # ABI selector for mint_initial(address)string
    
    # Encode student address as ABI argument
    student_bytes = decode_address(student_address)
    
    # Build app args
    app_args = [
        method_selector,
        student_bytes
    ]
    
    # Create application call transaction
    txn = ApplicationCallTxn(
        sender=admin_address,
        sp=params,
        index=HUSTLE_SCORE_APP_ID,
        on_complete=OnComplete.NoOpOC,
        app_args=app_args,
        boxes=[(HUSTLE_SCORE_APP_ID, student_bytes)]  # Box reference for MBR
    )
    
    # Sign and send
    signed_txn = txn.sign(admin_private_key)
    tx_id = client.send_transaction(signed_txn)
    
    # Wait for confirmation
    from algosdk import transaction
    transaction.wait_for_confirmation(client, tx_id, 4)
    
    print(f"✓ Initialized student {student_address} with 0 score")
    return tx_id


async def add_reputation_points(student_address: str, points: int = 10):
    """
    Add reputation points to a student's Hustle Score.
    This is called after a milestone is approved.
    """
    client = get_algod_client()
    admin_address, admin_private_key = get_admin_account()
    
    # Ensure student is initialized first
    await ensure_student_initialized(student_address)
    
    # Get suggested params
    params = client.suggested_params()
    
    # Prepare method call arguments
    method_selector = bytes.fromhex("7d4d30ad") # ABI selector for add_reputation(address,uint64)string
    student_bytes = decode_address(student_address)
    points_bytes = points.to_bytes(8, 'big')  # UInt64
    
    app_args = [
        method_selector,
        student_bytes,
        points_bytes
    ]
    
    # Create application call transaction
    txn = ApplicationCallTxn(
        sender=admin_address,
        sp=params,
        index=HUSTLE_SCORE_APP_ID,
        on_complete=OnComplete.NoOpOC,
        app_args=app_args,
        boxes=[(HUSTLE_SCORE_APP_ID, student_bytes)]  # Box reference
    )
    
    # Sign and send
    signed_txn = txn.sign(admin_private_key)
    tx_id = client.send_transaction(signed_txn)
    
    # Wait for confirmation
    from algosdk import transaction
    transaction.wait_for_confirmation(client, tx_id, 4)
    
    print(f"✓ Added {points} reputation points to {student_address}")
    return tx_id


async def get_student_score(student_address: str) -> int:
    """
    Query a student's Hustle Score from the blockchain.
    Returns 0 if student not initialized.
    """
    try:
        client = get_algod_client()
        student_bytes = decode_address(student_address)
        
        # Read box storage directly
        box_name = student_bytes
        box_value = client.application_box_by_name(HUSTLE_SCORE_APP_ID, box_name)
        
        # Decode UInt64 (8 bytes, big endian)
        score_bytes = base64.b64decode(box_value['value'])
        score = int.from_bytes(score_bytes, 'big')
        
        return score
    except Exception as e:
        # Box doesn't exist or error reading
        print(f"Student {student_address} not initialized or error: {e}")
        return 0


# For testing
async def test_hustle_score():
    """Test function to verify the service works."""
    test_student = "J2UCDAMJLFKOP7OLPZHTQ2BFF65P7A6LKDE4OQ6ART4Y4L2HTLDTV2Q4Y"
    
    print("Testing HustleScore service...")
    
    # Get current score
    score = await get_student_score(test_student)
    print(f"Current score: {score}")
    
    # Add points
    await add_reputation_points(test_student, 10)
    
    # Check new score
    new_score = await get_student_score(test_student)
    print(f"New score: {new_score}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_hustle_score())
