"""
CampusNexus - IPFS Integration via Pinata
Handles image uploads to IPFS for marketplace listings.
"""
import requests
from fastapi import UploadFile, HTTPException

from app.config import get_settings

# Get settings instance
settings = get_settings()

# Pinata API Configuration
PINATA_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
PINATA_GATEWAY = "https://gateway.pinata.cloud/ipfs/"


async def upload_to_ipfs(file: UploadFile) -> dict:
    """
    Upload a file to IPFS via Pinata.
    
    Args:
        file: The uploaded file from FastAPI
    
    Returns:
        dict: Contains 'cid' and 'gateway_url'
    
    Raises:
        HTTPException: If upload fails or API keys not configured
    """
    if not settings.pinata_api_key or not settings.pinata_secret:
        raise HTTPException(
            status_code=500,
            detail="Pinata API keys not configured. Set PINATA_API_KEY and PINATA_SECRET in .env"
        )
    
    # Prepare headers
    headers = {
        "pinata_api_key": settings.pinata_api_key,
        "pinata_secret_api_key": settings.pinata_secret,
    }
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Prepare multipart form data
        files = {
            "file": (file.filename, file_content, file.content_type)
        }
        
        # Upload to Pinata
        response = requests.post(
            PINATA_UPLOAD_URL,
            files=files,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        # Extract CID from response
        result = response.json()
        cid = result["IpfsHash"]
        
        return {
            "cid": cid,
            "gateway_url": f"{PINATA_GATEWAY}{cid}",
            "size": result.get("PinSize", 0)
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload to IPFS: {str(e)}"
        )
    except KeyError:
        raise HTTPException(
            status_code=500,
            detail="Invalid response from Pinata API"
        )
    finally:
        # Reset file pointer for potential reuse
        await file.seek(0)


def get_ipfs_url(cid: str) -> str:
    """
    Get the IPFS gateway URL for a given CID.
    
    Args:
        cid: IPFS Content Identifier
    
    Returns:
        str: Full gateway URL
    """
    return f"{PINATA_GATEWAY}{cid}"
