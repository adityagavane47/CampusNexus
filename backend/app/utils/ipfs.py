import requests
from fastapi import UploadFile, HTTPException

from app.config import get_settings

settings = get_settings()

PINATA_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
PINATA_GATEWAY = "https://gateway.pinata.cloud/ipfs/"

async def upload_to_ipfs(file: UploadFile) -> dict:

    if not settings.pinata_api_key or not settings.pinata_secret:
        raise HTTPException(
            status_code=500,
            detail="Pinata API keys not configured. Set PINATA_API_KEY and PINATA_SECRET in .env"
        )
    
    headers = {
        "pinata_api_key": settings.pinata_api_key,
        "pinata_secret_api_key": settings.pinata_secret,
    }
    
    try:
        file_content = await file.read()
        
        files = {
            "file": (file.filename, file_content, file.content_type)
        }
        
        response = requests.post(
            PINATA_UPLOAD_URL,
            files=files,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
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
        await file.seek(0)

def get_ipfs_url(cid: str) -> str:

    return f"{PINATA_GATEWAY}{cid}"
