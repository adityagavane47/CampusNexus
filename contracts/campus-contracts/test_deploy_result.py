from algokit_utils import AlgorandClient
from smart_contracts.artifacts.escrow.milestone_escrow_client import APP_SPEC
import os
from dotenv import load_dotenv

load_dotenv()

try:
    algorand = AlgorandClient.from_environment()
    mnemonic = os.getenv("DEPLOYER_MNEMONIC")
    deployer = algorand.account.from_mnemonic(mnemonic=mnemonic)
    
    factory = algorand.client.get_app_factory(
        app_spec=APP_SPEC,
        app_name="MilestoneEscrow",
        default_sender=deployer.address,
        default_signer=deployer.signer,
    )
    
    result, _ = factory.deploy(
        on_schema_break="append",
        on_update="append",
    )
    
    print(f"Result type: {type(result)}")
    print(f"Result dir: {[x for x in dir(result) if not x.startswith('_')]}")
    print(f"Result: {result}")
    if hasattr(result, 'app_id'):
        print(f"App ID: {result.app_id}")
    if hasattr(result, 'app'):
        print(f"App: {result.app}")
        if hasattr(result.app, 'app_id'):
            print(f"App.app_id: {result.app.app_id}")
            
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
