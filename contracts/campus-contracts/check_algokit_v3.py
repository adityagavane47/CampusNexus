from algokit_utils import AlgorandClient
import inspect

try:
    client = AlgorandClient.from_environment()
    sig = inspect.signature(client.account.from_mnemonic)
    print(f"Signature: {sig}")
except Exception as e:
    print(f"Error: {e}")
