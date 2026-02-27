import logging
import os
import json
import base64
from dotenv import load_dotenv
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from algosdk import transaction

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-10s: %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

def deploy_app_bare(algod_client, sender_address, sender_sk, approval_program, clear_program, global_schema, local_schema):

    params = algod_client.suggested_params()
    
    txn = transaction.ApplicationCreateTxn(
        sender=sender_address,
        sp=params,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=global_schema,
        local_schema=local_schema
    )
    
    signed_txn = txn.sign(sender_sk)
    tx_id = algod_client.send_transaction(signed_txn)
    logger.info(f"Transaction sent with ID: {tx_id}")
    
    result = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    app_id = result['application-index']
    app_address = logic.get_application_address(app_id)
    
    return app_id, app_address

def deploy_app_with_abi_create(algod_client, sender_address, sender_sk, approval_program, clear_program, global_schema, local_schema):

    params = algod_client.suggested_params()
    
    from algosdk.abi import Method
    method_obj = Method.from_signature("create()string")
    method_selector = method_obj.get_selector()
    
    txn = transaction.ApplicationCreateTxn(
        sender=sender_address,
        sp=params,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=global_schema,
        local_schema=local_schema,
        app_args=[method_selector]
    )
    
    signed_txn = txn.sign(sender_sk)
    tx_id = algod_client.send_transaction(signed_txn)
    logger.info(f"Transaction sent with ID: {tx_id}")
    
    result = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    app_id = result['application-index']
    app_address = logic.get_application_address(app_id)
    
    return app_id, app_address

def main():
    algod_address = "https://testnet-api.algonode.cloud"
    algod_token = ""
    algod_client = algod.AlgodClient(algod_token, algod_address)
    
    deployer_mnemonic = os.getenv("DEPLOYER_MNEMONIC")
    if not deployer_mnemonic:
        raise ValueError("DEPLOYER_MNEMONIC not set")
    
    deployer_sk = mnemonic.to_private_key(deployer_mnemonic)
    deployer_address = account.address_from_private_key(deployer_sk)
    logger.info(f"Deploying with account: {deployer_address}")
    
    with open("smart_contracts/artifacts/escrow/MilestoneEscrow.approval.teal", "r") as f:
        escrow_approval_teal = f.read()
    with open("smart_contracts/artifacts/escrow/MilestoneEscrow.clear.teal", "r") as f:
        escrow_clear_teal = f.read()
    
    logger.info("Compiling MilestoneEscrow programs...")
    escrow_approval = algod_client.compile(escrow_approval_teal)['result']
    escrow_clear = algod_client.compile(escrow_clear_teal)['result']
    escrow_approval_bytes = base64.b64decode(escrow_approval)
    escrow_clear_bytes = base64.b64decode(escrow_clear)
    
    logger.info("Deploying MilestoneEscrow...")
    escrow_app_id, escrow_app_address = deploy_app_bare(
        algod_client,
        deployer_address,
        deployer_sk,
        escrow_approval_bytes,
        escrow_clear_bytes,
        transaction.StateSchema(num_uints=3, num_byte_slices=2),
        transaction.StateSchema(num_uints=0, num_byte_slices=0)
    )
    logger.info(f"✅ Deployed MilestoneEscrow with app_id: {escrow_app_id}")
    
    with open("smart_contracts/artifacts/hustle_score/HustleScore.approval.teal", "r") as f:
        hustle_approval_teal = f.read()
    with open("smart_contracts/artifacts/hustle_score/HustleScore.clear.teal", "r") as f:
        hustle_clear_teal = f.read()
    
    logger.info("Compiling HustleScore programs...")
    hustle_approval = algod_client.compile(hustle_approval_teal)['result']
    hustle_clear = algod_client.compile(hustle_clear_teal)['result']
    hustle_approval_bytes = base64.b64decode(hustle_approval)
    hustle_clear_bytes = base64.b64decode(hustle_clear)
    
    logger.info("Deploying HustleScore...")
    hustle_app_id, hustle_app_address = deploy_app_with_abi_create(
        algod_client,
        deployer_address,
        deployer_sk,
        hustle_approval_bytes,
        hustle_clear_bytes,
        transaction.StateSchema(num_uints=1, num_byte_slices=1),
        transaction.StateSchema(num_uints=0, num_byte_slices=0)
    )
    logger.info(f"✅ Deployed HustleScore with app_id: {hustle_app_id}")
    
    deployed = {
        "network": "testnet",
        "contracts": {
            "MilestoneEscrow": {
                "app_id": escrow_app_id,
                "app_address": escrow_app_address,
                "deployer": deployer_address
            },
            "HustleScore": {
                "app_id": hustle_app_id,
                "app_address": hustle_app_address,
                "deployer": deployer_address
            }
        }
    }
    
    with open("deployed_contracts.json", "w") as f:
        json.dump(deployed, f, indent=2)
    
    logger.info(f"\n📝 Deployment complete! App IDs:")
    logger.info(f"   MilestoneEscrow: {escrow_app_id}")
    logger.info(f"   HustleScore: {hustle_app_id}")
    logger.info(f"\n✅ Deployment info saved to deployed_contracts.json")

if __name__ == "__main__":
    main()
