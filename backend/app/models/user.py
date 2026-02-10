"""
CampusNexus - User Model
OAuth and Wallet-based user management
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """User model for both OAuth and wallet authentication."""
    id: str  # Can be email or wallet address
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    wallet_address: Optional[str] = None
    
    # OAuth provider info
    oauth_provider: Optional[str] = None  # 'google', 'github', or None for wallet
    oauth_id: Optional[str] = None  # Provider-specific user ID
    
    # Timestamps
    created_at: datetime
    last_login: datetime
    
    # College info
    college: str = "VIT Pune"
    age: Optional[int] = None
    year: Optional[str] = None
    branch: Optional[str] = None
    
    # Profile enhancements
    skills: Optional[List[str]] = None
    profile_picture: Optional[str] = None  # Base64 or URL
    bio: Optional[str] = None  # About me section


class UserCreate(BaseModel):
    """Model for creating a new user."""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    wallet_address: Optional[str] = None
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None


class UserUpdate(BaseModel):
    """Model for updating user profile."""
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None
    branch: Optional[str] = None
    skills: Optional[List[str]] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    wallet_address: Optional[str] = None


class UserResponse(BaseModel):
    """Public user response model."""
    id: str
    email: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    wallet_address: Optional[str] = None
    oauth_provider: Optional[str] = None
    college: str
    age: Optional[int] = None
    year: Optional[str] = None
    branch: Optional[str] = None
    skills: Optional[List[str]] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime


class OAuthUserInfo(BaseModel):
    """OAuth user information from provider."""
    email: EmailStr
    name: str
    avatar: Optional[str] = None
    provider: str
    provider_id: str
