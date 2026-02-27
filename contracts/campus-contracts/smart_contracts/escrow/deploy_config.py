import logging
import algokit_utils
from smart_contracts.artifacts.escrow.milestone_escrow_client import MilestoneEscrowFactory

logger = logging.getLogger(__name__)

def deploy() -> None:

    algorand = algokit_utils.AlgorandClient.from_environment()
    
    deployer = algorand.account.from_environment("DEPLOYER")
    logger.info(f"Deploying with account: {deployer.address}")

    factory = algorand.client.get_typed_app_factory(
        MilestoneEscrowFactory, 
        default_sender=deployer.address
    )

    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    logger.info(
        f"{'Created' if result.operation_performed == algokit_utils.OperationPerformed.Create else 'Updated'} "
        f"MilestoneEscrow with app_id: {app_client.app_id}, "
        f"app_address: {app_client.app_address}"
    )

def get_localnet_default_account(algod_client):

    pass
