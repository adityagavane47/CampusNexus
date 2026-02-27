import logging
import algokit_utils
from smart_contracts.artifacts.hustle_score.hustle_score_client import HustleScoreFactory
import traceback
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        algorand = algokit_utils.AlgorandClient.from_environment()
        
        deployer = algorand.account.from_environment("DEPLOYER")
        logger.info(f"Deploying with account: {deployer.address}")
        
        factory = algorand.client.get_typed_app_factory(
            HustleScoreFactory, 
            default_sender=deployer.address
        )
        
        logger.info("Attempting to CREATE app via deploy with unique name...")
        
        app_client, result = factory.deploy(
             app_name="HustleScore-Clean-V2", 
             on_update=algokit_utils.OnUpdate.AppendApp,
             on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        )
        
        logger.info(f"Deployed successfully! App ID: {app_client.app_id}")
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
