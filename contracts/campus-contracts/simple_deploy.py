"""
Simple deployment script for MilestoneEscrow contract (LocalNet)
Run this directly to bypass caching issues: poetry run python simple_deploy.py
"""
import logging
import algokit_utils
from smart_contracts.artifacts.escrow.milestone_escrow_client import MilestoneEscrowFactory
from smart_contracts.artifacts.hustle_score.hustle_score_client import HustleScoreFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Deploy contracts to LocalNet."""
    
    # Initialize Algorand client (reads from .env)
    algorand = algokit_utils.AlgorandClient.from_environment()
    
    # Use LocalNet dispenser account (pre-funded)
    deployer = algorand.account.localnet_dispenser()
    logger.info(f"Deploying with LocalNet dispenser: {deployer.address}")
    
    # Deploy MilestoneEscrow
    logger.info("=" * 50)
    logger.info("Deploying MilestoneEscrow...")
    escrow_factory = algorand.client.get_typed_app_factory(
        MilestoneEscrowFactory,
        default_sender=deployer.address
    )
    
    escrow_client, escrow_result = escrow_factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )
    
    logger.info(f"✅ Deployed MilestoneEscrow!")
    logger.info(f"   App ID: {escrow_client.app_id}")
    logger.info(f"   App Address: {escrow_client.app_address}")
    
    # Deploy HustleScore
    logger.info("=" * 50)
    logger.info("Deploying HustleScore...")
    hustle_factory = algorand.client.get_typed_app_factory(
        HustleScoreFactory,
        default_sender=deployer.address
    )
    
    hustle_client, hustle_result = hustle_factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )
    
    logger.info(f"✅ Deployed HustleScore!")
    logger.info(f"   App ID: {hustle_client.app_id}")
    logger.info(f"   App Address: {hustle_client.app_address}")
    
    # Summary
    logger.info("=" * 50)
    logger.info("🎉 DEPLOYMENT COMPLETE!")
    logger.info("=" * 50)
    logger.info(f"MilestoneEscrow App ID: {escrow_client.app_id}")
    logger.info(f"HustleScore App ID: {hustle_client.app_id}")
    logger.info("")
    logger.info("✏️  UPDATE FRONTEND CONFIG:")
    logger.info(f"   Edit: frontend/src/services/algorand.js")
    logger.info(f"   Set: CONTRACT_IDS = {{")
    logger.info(f"       escrow: {escrow_client.app_id},")
    logger.info(f"       hustleScore: {hustle_client.app_id},")
    logger.info(f"   }}")
    

if __name__ == "__main__":
    main()
