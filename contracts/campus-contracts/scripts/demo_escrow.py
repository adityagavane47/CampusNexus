import sys
import os
import logging
from dotenv import load_dotenv
import base64
from algosdk import account, mnemonic, transaction
from algosdk.v2client import algod, indexer
from algosdk.atomic_transaction_composer import AccountTransactionSigner, AtomicTransactionComposer
from algosdk.abi import Method
import algokit_utils
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_contracts.artifacts.escrow.milestone_escrow_client import (
    MilestoneEscrowFactory,
    MilestoneEscrowClient,
    CreateEscrowArgs,
    ReleasePaymentArgs
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-10s: %(message)s")
logger = logging.getLogger(__name__)

def get_accounts():

    load_dotenv()
    
    deployer_mnemonic = os.getenv("DEPLOYER_MNEMONIC")
    if not deployer_mnemonic:
        raise ValueError("DEPLOYER_MNEMONIC not set in .env")
        
    deployer_sk = mnemonic.to_private_key(deployer_mnemonic)
    deployer_addr = account.address_from_private_key(deployer_sk)
    
    freelancer_sk, freelancer_addr = account.generate_account()
    
    return (deployer_sk, deployer_addr), (freelancer_sk, freelancer_addr)

def main():
    logger.info(" Starting Escrow Demo Script")
    
    os.environ["ALGOD_SERVER"] = "https://testnet-api.algonode.cloud"
    os.environ["ALGOD_TOKEN"] = ""
    os.environ["INDEXER_SERVER"] = "https://testnet-idx.algonode.cloud"
    os.environ["INDEXER_TOKEN"] = ""
    os.environ["ALGOD_ADDRESS"] = "https://testnet-api.algonode.cloud"
    os.environ["INDEXER_ADDRESS"] = "https://testnet-idx.algonode.cloud"
    
    algorand = algokit_utils.AlgorandClient.from_environment()
    
    (client_sk, client_addr), (freelancer_sk, freelancer_addr) = get_accounts()
    logger.info(f"Client (You): {client_addr}")
    logger.info(f"Freelancer (Simulated): {freelancer_addr}")
    
    signer = AccountTransactionSigner(client_sk)

    logger.info("\n1️ Deploying Milestone Escrow Contract...")
    factory = MilestoneEscrowFactory(
        algorand=algorand,
        default_sender=client_addr,
        default_signer=signer
    )
    
    try:
        app_client, result = factory.send.create.bare()
        app_id = app_client.app_id
        app_addr = app_client.app_address
        logger.info(f"✅ Escrow Deployed! App ID: {app_id}")
        logger.info(f"   Escrow Address: {app_addr}")
        logger.info(f"   Creation TxID: {result.tx_id}")
        
        logger.info("   Initializing Escrow parameters...")
        atc = AtomicTransactionComposer()
        atc.add_method_call(
            app_id=app_id,
            method=Method.from_signature("create_escrow(address,uint64)string"),
            sender=client_addr,
            sp=algorand.client.algod.suggested_params(),
            signer=signer,
            method_args=[freelancer_addr, 1000000]
        )
        init_result = atc.execute(algorand.client.algod, wait_rounds=4)
        logger.info(f"✅ Escrow Initialized! TxID: {init_result.tx_ids[0]}")
        
    except Exception as e:
        logger.error(f"❌ Deployment Failed: {e}")
        traceback.print_exc()
        return
    
    logger.info("\n2️  Funding Escrow (Client -> Contract)...")
    logger.info("   Sending 1.2 ALGO (1.0 for payment + 0.2 for MBR/Fees)...")
    
    try:
        atc = AtomicTransactionComposer()
        atc.add_method_call(
            app_id=app_id,
            method=Method.from_signature("fund_escrow()string"),
            sender=client_addr,
            sp=algorand.client.algod.suggested_params(),
            signer=signer,
            method_args=[]
        )
        result = atc.execute(algorand.client.algod, wait_rounds=4)
        logger.info(f"✅ Escrow Funded! TxID: {result.tx_ids[0]}")
    except Exception as e:
        logger.warning(f"⚠️  Funding via client method failed (Likely artifact mismatch): {e}")
        logger.info("   Attempting manual funding transaction...")
        try:
             
             res = algorand.send.payment(
                 algokit_utils.PaymentParams(
                     sender=client_addr,
                     receiver=app_addr,
                     amount=1_200_000,
                     signer=signer
                 )
             )
             logger.info(f"✅ Manual Funding Successful. TxID: {res.tx_id}")
        except Exception as e2:
             logger.error(f"❌ Funding Failed: {e2}")
             return

    logger.info("\n3️⃣  Releasing Payment (Client Approval)...")
    try:
        atc = AtomicTransactionComposer()
        atc.add_method_call(
            app_id=app_id,
            method=Method.from_signature("release_payment(uint64)string"),
            sender=client_addr,
            sp=algorand.client.algod.suggested_params(),
            signer=signer,
            method_args=[1000000]
        )
        result = atc.execute(algorand.client.algod, wait_rounds=4)
        logger.info(f"✅ Payment Released! TxID: {result.tx_ids[0]}")
        logger.info("   Funds transferred to freelancer.")
    except Exception as e:
        logger.error(f"❌ Release Failed: {e}")
        traceback.print_exc()
        return
        
    logger.info("\n🎉 Demo Complete!")

if __name__ == "__main__":
    main()
