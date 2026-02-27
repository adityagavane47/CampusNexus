import algosdk
import time

ADDRESS = "SCVK26XPYHJ4MIAPSJWFUDGV2UV6ETE7PGMAPCNWYL62JVXC7OCCBDKERA"

def check_balance():
    algod_address = "https://testnet-api.algonode.cloud"
    algod_token = ""
    algod_client = algosdk.v2client.algod.AlgodClient(algod_token, algod_address)
    
    try:
        account_info = algod_client.account_info(ADDRESS)
        amount = account_info.get('amount', 0)
        print(f"Balance for {ADDRESS}: {amount} microAlgos ({amount/1_000_000} ALGO)")
    except Exception as e:
        print(f"Error checking balance: {e}")

if __name__ == "__main__":
    check_balance()
