from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class User(BaseModel):

    id: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    wallet_address: Optional[str] = None
    
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None
    
    created_at: datetime
    last_login: datetime
    
    college: str = ""
    age: Optional[int] = None
    year: Optional[str] = None
    branch: Optional[str] = None
    
    skills: Optional[List[str]] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(BaseModel):

    email: Optional[EmailStr] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    wallet_address: Optional[str] = None
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None

class UserUpdate(BaseModel):

    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None
    branch: Optional[str] = None
    skills: Optional[List[str]] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    wallet_address: Optional[str] = None

class UserResponse(BaseModel):

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

    email: EmailStr
    name: str
    avatar: Optional[str] = None
    provider: str
    provider_id: str
