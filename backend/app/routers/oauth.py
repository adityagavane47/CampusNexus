"""
CampusNexus - OAuth Authentication Router
Google and GitHub OAuth 2.0 authentication
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from jose import jwt
from pydantic import BaseModel

from app.config import get_settings
from app.models.user import UserCreate, UserResponse, OAuthUserInfo, UserUpdate
from app.utils.database import (
    find_user_by_email, 
    find_user_by_oauth, 
    create_user,
    update_user_login,
    update_user_profile
)

router = APIRouter()
settings = get_settings()

# Initialize OAuth
oauth = OAuth()

# Register Google OAuth
if settings.google_client_id and settings.google_client_secret:
    oauth.register(
        name='google',
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

# Register GitHub OAuth
if settings.github_client_id and settings.github_client_secret:
    oauth.register(
        name='github',
        client_id=settings.github_client_id,
        client_secret=settings.github_client_secret,
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )


def create_access_token(user_id: str, email: str = None) -> str:
    """Create JWT access token for authenticated user."""
    expires_delta = timedelta(minutes=settings.jwt_expire_minutes)
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
        "college": settings.college_name,
    }
    
    access_token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return access_token


@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth login flow."""
    if not settings.google_client_id:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    
    redirect_uri = f"{settings.oauth_redirect_uri}/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback."""
    try:
        # Get access token from Google
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info from Google")
        
        email = user_info.get('email')
        name = user_info.get('name')
        avatar = user_info.get('picture')
        google_id = user_info.get('sub')
        
        # Find or create user
        user = find_user_by_oauth('google', google_id)
        
        if not user:
            # Check if user exists with this email
            user = find_user_by_email(email)
            
            if not user:
                # Create new user
                user_create = UserCreate(
                    email=email,
                    name=name,
                    avatar=avatar,
                    oauth_provider='google',
                    oauth_id=google_id
                )
                user = create_user(user_create)
            else:
                # Update existing user with Google OAuth
                update_user_login(user.id)
        else:
            # Update last login
            update_user_login(user.id)
        
        # Create JWT token
        access_token = create_access_token(user.id, user.email)
        
        # Redirect to frontend with token
        redirect_url = f"{settings.frontend_url}?token={access_token}&provider=google"
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        print(f"Google OAuth error: {e}")
        error_url = f"{settings.frontend_url}?error=oauth_failed"
        return RedirectResponse(url=error_url)


@router.get("/github/login")
async def github_login(request: Request):
    """Initiate GitHub OAuth login flow."""
    if not settings.github_client_id:
        raise HTTPException(status_code=500, detail="GitHub OAuth not configured")
    
    redirect_uri = f"{settings.oauth_redirect_uri}/github/callback"
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def github_callback(request: Request):
    """Handle GitHub OAuth callback."""
    try:
        # Get access token from GitHub
        token = await oauth.github.authorize_access_token(request)
        
        # Get user info from GitHub
        resp = await oauth.github.get('user', token=token)
        user_info = resp.json()
        
        # Get user email (might need separate API call)
        email_resp = await oauth.github.get('user/emails', token=token)
        emails = email_resp.json()
        
        # Get primary email
        primary_email = None
        for email_data in emails:
            if email_data.get('primary'):
                primary_email = email_data.get('email')
                break
        
        if not primary_email and emails:
            primary_email = emails[0].get('email')
        
        github_id = str(user_info.get('id'))
        name = user_info.get('name') or user_info.get('login')
        avatar = user_info.get('avatar_url')
        
        # Find or create user
        user = find_user_by_oauth('github', github_id)
        
        if not user:
            # Check if user exists with this email
            if primary_email:
                user = find_user_by_email(primary_email)
            
            if not user:
                # Create new user
                user_create = UserCreate(
                    email=primary_email,
                    name=name,
                    avatar=avatar,
                    oauth_provider='github',
                    oauth_id=github_id
                )
                user = create_user(user_create)
            else:
                # Update existing user with GitHub OAuth
                update_user_login(user.id)
        else:
            # Update last login
            update_user_login(user.id)
        
        # Create JWT token
        access_token = create_access_token(user.id, user.email)
        
        # Redirect to frontend with token
        redirect_url = f"{settings.frontend_url}?token={access_token}&provider=github"
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        print(f"GitHub OAuth error: {e}")
        error_url = f"{settings.frontend_url}?error=oauth_failed"
        return RedirectResponse(url=error_url)


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: str):
    """Get current authenticated user info."""
    from app.utils.database import load_users
    
    users = load_users()
    for user_data in users:
        if user_data.get('id') == user_id:
            return UserResponse(**user_data)
    
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/profile", response_model=UserResponse)
async def update_profile(user_id: str, profile: UserUpdate):
    """Update user profile."""
    # In a real app, verify that the current user matches user_id via JWT
    
    # We need to convert pydantic model to dict, excluding unset fields
    update_data = profile.model_dump(exclude_unset=True)
    
    updated_user = update_user_profile(user_id, update_data)
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**updated_user.model_dump())


class ProfilePictureUpload(BaseModel):
    """Model for profile picture upload."""
    user_id: str
    image_data: str  # Base64 encoded image


@router.post("/upload-profile-picture")
async def upload_profile_picture(upload: ProfilePictureUpload):
    """
    Upload profile picture (Base64 encoded).
    In production, this should upload to cloud storage and return URL.
    """
    try:
        # For now, we'll store the Base64 string directly
        # In production, decode and upload to S3/Cloudinary
        
        updated_user = update_user_profile(
            upload.user_id, 
            {"profile_picture": upload.image_data}
        )
        
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "success": True,
            "profile_picture": upload.image_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

