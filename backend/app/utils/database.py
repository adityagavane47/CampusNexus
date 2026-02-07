"""
CampusNexus - Simple JSON Database Utilities
For development purposes - replace with proper database in production
"""
import json
import os
from datetime import datetime
from typing import Optional, Dict, List
from pathlib import Path

from app.models.user import User, UserCreate


# Database file path
DB_FILE = Path(__file__).parent.parent.parent / "data" / "users.json"


def ensure_db_exists():
    """Ensure the database file and directory exist."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DB_FILE.exists():
        DB_FILE.write_text(json.dumps({"users": []}))


def load_users() -> List[Dict]:
    """Load all users from the database."""
    ensure_db_exists()
    with open(DB_FILE, 'r') as f:
        data = json.load(f)
    return data.get("users", [])


def save_users(users: List[Dict]):
    """Save all users to the database."""
    ensure_db_exists()
    with open(DB_FILE, 'w') as f:
        json.dump({"users": users}, f, indent=2, default=str)


def find_user_by_email(email: str) -> Optional[User]:
    """Find a user by email."""
    users = load_users()
    for user_data in users:
        if user_data.get("email") == email:
            return User(**user_data)
    return None


def find_user_by_oauth(provider: str, provider_id: str) -> Optional[User]:
    """Find a user by OAuth provider and ID."""
    users = load_users()
    for user_data in users:
        if (user_data.get("oauth_provider") == provider and 
            user_data.get("oauth_id") == provider_id):
            return User(**user_data)
    return None


def find_user_by_wallet(wallet_address: str) -> Optional[User]:
    """Find a user by wallet address."""
    users = load_users()
    for user_data in users:
        if user_data.get("wallet_address") == wallet_address:
            return User(**user_data)
    return None


def create_user(user_create: UserCreate) -> User:
    """Create a new user."""
    users = load_users()
    
    # Generate user ID (use email or wallet address)
    user_id = user_create.email or user_create.wallet_address
    
    now = datetime.utcnow()
    
    user = User(
        id=user_id,
        email=user_create.email,
        name=user_create.name,
        avatar=user_create.avatar,
        wallet_address=user_create.wallet_address,
        oauth_provider=user_create.oauth_provider,
        oauth_id=user_create.oauth_id,
        created_at=now,
        last_login=now,
        college="VIT Pune"
    )
    
    users.append(user.model_dump())
    save_users(users)
    
    return user


def update_user_login(user_id: str) -> Optional[User]:
    """Update user's last login time."""
    users = load_users()
    
    for i, user_data in enumerate(users):
        if user_data.get("id") == user_id:
            user_data["last_login"] = datetime.utcnow().isoformat()
            users[i] = user_data
            save_users(users)
            return User(**user_data)
    
    return None


def update_user_profile(user_id: str, updates: Dict) -> Optional[User]:
    """Update user profile fields."""
    users = load_users()
    
    for i, user_data in enumerate(users):
        if user_data.get("id") == user_id:
            # Update fields
            for key, value in updates.items():
                if value is not None:
                    user_data[key] = value
            
            users[i] = user_data
            save_users(users)
            return User(**user_data)
    
    return None


def get_all_users() -> List[User]:
    """Get all users (for admin purposes)."""
    users = load_users()
    return [User(**user_data) for user_data in users]
