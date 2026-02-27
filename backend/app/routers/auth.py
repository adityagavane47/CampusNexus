from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt

from app.config import get_settings
from app.services.algorand import verify_wallet_signature, get_account_info

from app.utils.database import (
    find_user_by_wallet,
    create_user,
    update_user_login,
    UserCreate
)

router = APIRouter()
settings = get_settings()

class WalletConnectRequest(BaseModel):

    address: str
    message: str
    signature: str

class AuthResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"
    address: str
    expires_in: int

class NonceResponse(BaseModel):

    nonce: str
    message: str

@router.get("/nonce/{address}", response_model=NonceResponse)
async def get_nonce(address: str):

    timestamp = datetime.utcnow().isoformat()
    message = f"Sign this message to authenticate with CampusNexus\nAddress: {address}\nTimestamp: {timestamp}\nCollege: {settings.college_name}"
    
    return NonceResponse(
        nonce=timestamp,
        message=message
    )

@router.post("/verify", response_model=AuthResponse)
async def verify_wallet(request: WalletConnectRequest):

    is_valid = verify_wallet_signature(
        request.address,
        request.message,
        request.signature
    )
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    account_info = get_account_info(request.address)
    if "error" in account_info:
        raise HTTPException(status_code=400, detail="Invalid Algorand address")
    
    
    expires_delta = timedelta(minutes=settings.jwt_expire_minutes)
    expire = datetime.utcnow() + expires_delta
    
    user = find_user_by_wallet(request.address)
    if not user:
        user_create = UserCreate(
            wallet_address=request.address,
            name=f"Wallet User {request.address[:4]}...{request.address[-4:]}",
            email=None,
            avatar=None,
            oauth_provider="algorand",
            oauth_id=request.address
        )
        create_user(user_create)
    else:
        update_user_login(user.id)
    
    payload = {
        "sub": request.address,
        "exp": expire,
        "iat": datetime.utcnow(),
        "college": settings.college_name,
    }
    
    access_token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return AuthResponse(
        access_token=access_token,
        address=request.address,
        expires_in=settings.jwt_expire_minutes * 60
    )

@router.get("/me")
async def get_current_user(address: str):

    account_info = get_account_info(address)
    
    return {
        "address": address,
        "balance": account_info.get("amount", 0) / 1_000_000,
        "college": settings.college_name,
    }
