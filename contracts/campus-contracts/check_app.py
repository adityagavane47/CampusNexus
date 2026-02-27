import logging
import algokit_utils
from smart_contracts.artifacts.hustle_score.hustle_score_client import HustleScoreFactory
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    algorand = algokit_utils.AlgorandClient.from_environment()
    app_id = 755519100
    
    logger.info(f"Checking App ID: {app_id}")
    
    try:
        global_state = algorand.app.get_global_state(app_id)
        logger.info(f"Global State: {global_state}")
             
       
        admin_value = global_state.get('admin')
        logger.info(f"Admin Value: {admin_value}")
             
        if admin_value:
             logger.info("Admin key found!")
                 
    except Exception as e:
        logger.error(f"Failed to get global state: {e}")
        try:
             pass
        except:
             pass
        
    except Exception as e:
        logger.error(f"Failed to get app info: {e}")

if __name__ == "__main__":
    main()
