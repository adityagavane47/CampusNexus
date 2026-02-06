import logging

from smart_contracts.escrow.contract import MilestoneEscrow

logger = logging.getLogger(__name__)


def deploy() -> None:
    """Deploy the MilestoneEscrow contract."""
    from algokit_utils import (
        OnSchemaBreak,
        OnUpdate,
        get_algod_client,
        get_indexer_client,
    )
    from algokit_utils.applications.app_client import AppClient
    from algokit_utils.config import config
    
    config.configure(populate_app_call_resources=True)
    
    algod_client = get_algod_client()

    app_client = AppClient.from_client_and_contract(
        algod_client=algod_client,
        contract=MilestoneEscrow(),
        creator=get_localnet_default_account(algod_client),
    )

    app_client.deploy(
        on_schema_break=OnSchemaBreak.AppendApp,
        on_update=OnUpdate.AppendApp,
    )

    logger.info(f"Deployed MilestoneEscrow with app_id: {app_client.app_id}")


def get_localnet_default_account(algod_client):
    """Get the default localnet account."""
    from algokit_utils import get_localnet_default_account as get_default
    return get_default(algod_client)
