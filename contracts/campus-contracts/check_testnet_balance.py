from algokit_utils import AlgorandClient
import os
from dotenv import load_dotenv

load_dotenv()

try:
    client = AlgorandClient.from_environment()
    mnemonic = os.getenv("DEPLOYER_MNEMONIC")
    if mnemonic:
        acct = client.account.from_mnemonic(mnemonic=mnemonic)
        info = client.account.get_information(acct.address)
        print(f"Address: {acct.address}")
        print(f"Balance: {info.amount} microAlgos")
        print(f"Balance: {info.amount.micro_algo/1_000_000} ALGO")
    else:
        print("No DEPLOYER_MNEMONIC set")
except Exception as e:
    print(f"Error: {e}")
