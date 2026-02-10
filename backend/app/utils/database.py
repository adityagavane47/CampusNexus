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
from app.models.notification import Notification, NotificationCreate


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


# ===== PROJECT DATABASE FUNCTIONS =====

# Project database file path
PROJECTS_DB_FILE = Path(__file__).parent.parent.parent / "data" / "projects.json"


def ensure_projects_db_exists():
    """Ensure the projects database file exists."""
    PROJECTS_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not PROJECTS_DB_FILE.exists():
        PROJECTS_DB_FILE.write_text(json.dumps({"projects": []}))


def load_projects() -> List[Dict]:
    """Load all projects from the database."""
    ensure_projects_db_exists()
    with open(PROJECTS_DB_FILE, 'r') as f:
        data = json.load(f)
    return data.get("projects", [])


def save_projects(projects: List[Dict]):
    """Save all projects to the database."""
    ensure_projects_db_exists()
    with open(PROJECTS_DB_FILE, 'w') as f:
        json.dump({"projects": projects}, f, indent=2, default=str)


def create_project(project_data: Dict) -> Dict:
    """Create a new project."""
    projects = load_projects()
    
    # Generate project ID
    project_id = len(projects) + 1
    
    # Get creator details from users database
    creator = None
    users = load_users()
    for user_data in users:
        if user_data.get("id") == project_data.get("creator_id"):
            creator = user_data
            break
    
    new_project = {
        "id": project_id,
        "title": project_data.get("title"),
        "description": project_data.get("description"),
        "skills_required": project_data.get("skills_required", []),
        "budget_algo": project_data.get("budget_algo"),
        "deadline": project_data.get("deadline"),
        "milestones": project_data.get("milestones", []),
        "creator_id": project_data.get("creator_id"),
        "creator_name": creator.get("name") if creator else "Unknown",
        "creator_avatar": creator.get("profile_picture") or creator.get("avatar") if creator else None,
        "status": "open",
        "created_at": datetime.utcnow().isoformat(),
        "applications": []
    }
    
    projects.append(new_project)
    save_projects(projects)
    
    return new_project


def get_all_projects() -> List[Dict]:
    """Get all projects."""
    return load_projects()


def get_project_by_id(project_id: int) -> Optional[Dict]:
    """Get a specific project by ID."""
    projects = load_projects()
    for project in projects:
        if project.get("id") == project_id:
            return project
    return None


def apply_to_project(project_id: int, applicant_id: str) -> Optional[Dict]:
    """Apply to a project."""
    projects = load_projects()
    
    # Get applicant details
    applicant = None
    users = load_users()
    for user_data in users:
        if user_data.get("id") == applicant_id:
            applicant = user_data
            break
    
    if not applicant:
        return None
    
    for i, project in enumerate(projects):
        if project.get("id") == project_id:
            # Check if already applied
            for app in project.get("applications", []):
                if app.get("user_id") == applicant_id:
                    return project  # Already applied
            
            # Add application
            application = {
                "user_id": applicant_id,
                "user_name": applicant.get("name", "Unknown"),
                "user_avatar": applicant.get("profile_picture") or applicant.get("avatar"),
                "applied_at": datetime.utcnow().isoformat()
            }
            
            if "applications" not in project:
                project["applications"] = []
            
            project["applications"].append(application)
            projects[i] = project
            save_projects(projects)
            
            # Create notification for project creator
            if str(project.get("creator_id")) != str(applicant_id):
                create_notification(NotificationCreate(
                    user_id=project.get("creator_id"),
                    title="New Application",
                    message=f"{applicant.get('name', 'Someone')} applied to your project: {project.get('title')}",
                    type="application",
                    related_id=str(project_id)
                ))
                
            return project
    

    return None


# ===== NOTIFICATION DATABASE FUNCTIONS =====

# Notification database file path
NOTIFICATIONS_DB_FILE = Path(__file__).parent.parent.parent / "data" / "notifications.json"


def ensure_notifications_db_exists():
    """Ensure the notifications database file exists."""
    NOTIFICATIONS_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not NOTIFICATIONS_DB_FILE.exists():
        NOTIFICATIONS_DB_FILE.write_text(json.dumps({"notifications": []}))


def load_notifications() -> List[Dict]:
    """Load all notifications from the database."""
    ensure_notifications_db_exists()
    with open(NOTIFICATIONS_DB_FILE, 'r') as f:
        data = json.load(f)
    return data.get("notifications", [])


def save_notifications(notifications: List[Dict]):
    """Save all notifications to the database."""
    ensure_notifications_db_exists()
    with open(NOTIFICATIONS_DB_FILE, 'w') as f:
        json.dump({"notifications": notifications}, f, indent=2, default=str)


def create_notification(notification_data: NotificationCreate) -> Notification:
    """Create a new notification."""
    notifications = load_notifications()
    
    # Generate notification ID
    notification_id = str(len(notifications) + 1)
    
    now = datetime.utcnow().isoformat()
    
    notification = Notification(
        id=notification_id,
        user_id=notification_data.user_id,
        title=notification_data.title,
        message=notification_data.message,
        type=notification_data.type,
        related_id=notification_data.related_id,
        is_read=False,
        created_at=now
    )
    
    notifications.append(notification.model_dump())
    save_notifications(notifications)
    
    return notification


def get_user_notifications(user_id: str) -> List[Notification]:
    """Get all notifications for a specific user, sorted by date (newest first)."""
    notifications = load_notifications()
    user_notifications = [n for n in notifications if n.get("user_id") == user_id]
    
    # Sort by created_at descending
    user_notifications.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return [Notification(**n) for n in user_notifications]


def mark_notification_read(notification_id: str) -> Optional[Notification]:
    """Mark a notification as read."""
    notifications = load_notifications()
    
    for i, notif_data in enumerate(notifications):
        if notif_data.get("id") == notification_id:
            notif_data["is_read"] = True
            notifications[i] = notif_data
            save_notifications(notifications)
            return Notification(**notif_data)
            
    return None


def get_unread_count(user_id: str) -> int:
    """Get count of unread notifications for a user."""
    notifications = load_notifications()
    return sum(1 for n in notifications if n.get("user_id") == user_id and not n.get("is_read"))


