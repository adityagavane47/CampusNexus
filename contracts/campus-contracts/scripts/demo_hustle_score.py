import sys
import os
import logging
from dotenv import load_dotenv
from algosdk import account, mnemonic
from algosdk.v2client import algod, indexer
from algosdk.atomic_transaction_composer import AccountTransactionSigner, AtomicTransactionComposer
from algosdk.abi import Method
import algokit_utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_contracts.artifacts.hustle_score.hustle_score_client import (
    HustleScoreFactory,
    HustleScoreClient,
    MintInitialArgs,
    AddReputationArgs,
    GetScoreArgs
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-10s: %(message)s")
logger = logging.getLogger(__name__)

def get_deployer():
    load_dotenv()
    deployer_mnemonic = os.getenv("DEPLOYER_MNEMONIC")
    if not deployer_mnemonic:
        raise ValueError("DEPLOYER_MNEMONIC not set in .env")
    
    deployer_sk = mnemonic.to_private_key(deployer_mnemonic)
    deployer_addr = account.address_from_private_key(deployer_sk)
    return deployer_sk, deployer_addr

def main():
    logger.info("🚀 Starting Hustle Score Demo")
    
    os.environ["ALGOD_SERVER"] = "https://testnet-api.algonode.cloud"
    os.environ["ALGOD_TOKEN"] = ""
    os.environ["INDEXER_SERVER"] = "https://testnet-idx.algonode.cloud"
    os.environ["INDEXER_TOKEN"] = ""
    os.environ["ALGOD_ADDRESS"] = "https://testnet-api.algonode.cloud"
    os.environ["INDEXER_ADDRESS"] = "https://testnet-idx.algonode.cloud"
    
    algorand = algokit_utils.AlgorandClient.from_environment()
    
    deployer_sk, deployer_addr = get_deployer()
    signer = AccountTransactionSigner(deployer_sk)
    logger.info(f"Admin (You): {deployer_addr}")
    
    logger.info("\n1️⃣  Deploying Hustle Score Contract...")
    factory = HustleScoreFactory(
        algorand=algorand,
        default_sender=deployer_addr,
        default_signer=signer
    )
    
    
    
    try:
        app_client, result = factory.send.create.bare()
        app_id = app_client.app_id
        logger.info(f"✅ HustleScore Deployed! App ID: {app_id}")
        logger.info(f"   Creation TxID: {result.tx_id}")

    except Exception as e:
        logger.error(f"❌ Deployment Failed: {e}")
        return
    
    student_sk, student_addr = account.generate_account()
    logger.info(f"\n2️⃣  Minting Soulbound Token for Student: {student_addr}")
    
    try:
        atc = AtomicTransactionComposer()
        atc.add_method_call(
            app_id=app_id,
            method=Method.from_signature("mint_initial(address)string"),
            sender=deployer_addr,
            sp=algorand.client.algod.suggested_params(),
            signer=signer,
            method_args=[student_addr]
        )
        result = atc.execute(algorand.client.algod, wait_rounds=4)
        logger.info(f"   Mint Result: {result.abi_results[0].return_value}")
    except Exception as e:
        logger.error(f"   Mint Failed: {e}")
        return

    logger.info("\n3️⃣  Adding Reputation Points (+10)...")
    try:
        atc = AtomicTransactionComposer()
        atc.add_method_call(
            app_id=app_id,
            method=Method.from_signature("add_reputation(address,uint64)string"),
            sender=deployer_addr,
            sp=algorand.client.algod.suggested_params(),
            signer=signer,
            method_args=[student_addr, 10]
        )
        result = atc.execute(algorand.client.algod, wait_rounds=4)
        logger.info(f"   Add Reputation Result: {result.abi_results[0].return_value}")
    except Exception as e:
        logger.error(f"   Add Reputation Failed: {e}")
        return

    logger.info("\n4️⃣  Verifying Score (Read Local State/Box)...")
    try:
        atc = AtomicTransactionComposer()
        atc.add_method_call(
            app_id=app_id,
            method=Method.from_signature("get_score(address)uint64"),
            sender=deployer_addr,
            sp=algorand.client.algod.suggested_params(),
            signer=signer,
            method_args=[student_addr]
        )
        result = atc.execute(algorand.client.algod, wait_rounds=4)
        logger.info(f"   Current Score for {student_addr[:8]}...: {result.abi_results[0].return_value}")
        
    except Exception as e:
        logger.error(f"   Get Score Failed: {e}")

    logger.info("\n🎉 Demo Complete!")

if __name__ == "__main__":
    main()
