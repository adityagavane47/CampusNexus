import logging
import os
from algokit_utils import AlgorandClient
from smart_contracts.artifacts.hustle_score.hustle_score_client import APP_SPEC

logger = logging.getLogger(__name__)


def deploy() -> None:
    """Deploy the HustleScore SBT contract."""
    
    # Use environment variables for connection
    algorand = AlgorandClient.from_environment()

    # Get deployer account
    mnemonic_phrase = os.getenv("DEPLOYER_MNEMONIC")
    if mnemonic_phrase:
        deployer = algorand.account.from_mnemonic(mnemonic=mnemonic_phrase)
        logger.info(f"Deploying with account: {deployer.address}")
    else:
        deployer = algorand.account.localnet_dispenser()
        logger.info(f"Deploying with Localnet dispenser: {deployer.address}")

    # Create App Factory
    factory = algorand.client.get_app_factory(
        app_spec=APP_SPEC,
        app_name="HustleScore",
        default_sender=deployer.address,
        default_signer=deployer.signer,
    )

    # Deploy using create (simpler, avoids network lookup)
    app = factory.create()

    logger.info(f"Deployed HustleScore with app_id: {app.app_id}")


def get_localnet_default_account(algod_client):
    """Deprecated helper."""
    pass
