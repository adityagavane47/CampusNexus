import json
import os
from datetime import datetime
from typing import Optional, Dict, List
from pathlib import Path

from app.models.user import User, UserCreate
from app.models.notification import Notification, NotificationCreate

DB_FILE = Path(__file__).parent.parent.parent / "data" / "users.json"

def ensure_db_exists():

    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DB_FILE.exists():
        DB_FILE.write_text(json.dumps({"users": []}))

def load_users() -> List[Dict]:

    ensure_db_exists()
    with open(DB_FILE, 'r') as f:
        data = json.load(f)
    return data.get("users", [])

def save_users(users: List[Dict]):

    ensure_db_exists()
    with open(DB_FILE, 'w') as f:
        json.dump({"users": users}, f, indent=2, default=str)

def find_user_by_email(email: str) -> Optional[User]:

    users = load_users()
    for user_data in users:
        if user_data.get("email") == email:
            return User(**user_data)
    return None

def find_user_by_oauth(provider: str, provider_id: str) -> Optional[User]:

    users = load_users()
    for user_data in users:
        if (user_data.get("oauth_provider") == provider and 
            user_data.get("oauth_id") == provider_id):
            return User(**user_data)
    return None

def find_user_by_wallet(wallet_address: str) -> Optional[User]:

    users = load_users()
    for user_data in users:
        if user_data.get("wallet_address") == wallet_address:
            return User(**user_data)
    return None

def create_user(user_create: UserCreate) -> User:

    users = load_users()
    
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
        college=""
    )
    
    users.append(user.model_dump())
    save_users(users)
    
    return user

def update_user_login(user_id: str) -> Optional[User]:

    users = load_users()
    
    for i, user_data in enumerate(users):
        if user_data.get("id") == user_id:
            user_data["last_login"] = datetime.utcnow().isoformat()
            users[i] = user_data
            save_users(users)
            return User(**user_data)
    
    return None

def update_user_profile(user_id: str, updates: Dict) -> Optional[User]:

    users = load_users()
    
    for i, user_data in enumerate(users):
        if user_data.get("id") == user_id:
            for key, value in updates.items():
                user_data[key] = value
            
            users[i] = user_data
            save_users(users)
            return User(**user_data)
    
    return None

def get_all_users() -> List[User]:

    users = load_users()
    return [User(**user_data) for user_data in users]

PROJECTS_DB_FILE = Path(__file__).parent.parent.parent / "data" / "projects.json"

def ensure_projects_db_exists():

    PROJECTS_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not PROJECTS_DB_FILE.exists():
        PROJECTS_DB_FILE.write_text(json.dumps({"projects": []}))

def load_projects() -> List[Dict]:

    ensure_projects_db_exists()
    with open(PROJECTS_DB_FILE, 'r') as f:
        data = json.load(f)
    return data.get("projects", [])

def save_projects(projects: List[Dict]):

    ensure_projects_db_exists()
    with open(PROJECTS_DB_FILE, 'w') as f:
        json.dump({"projects": projects}, f, indent=2, default=str)

def create_project(project_data: Dict) -> Dict:

    projects = load_projects()
    
    project_id = len(projects) + 1
    
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
        "escrow_app_id": project_data.get("escrow_app_id"),
        "status": "open",
        "created_at": datetime.utcnow().isoformat(),
        "applications": []
    }
    
    projects.append(new_project)
    save_projects(projects)
    
    return new_project

def get_all_projects() -> List[Dict]:

    return load_projects()

def get_project_by_id(project_id: int) -> Optional[Dict]:

    projects = load_projects()
    for project in projects:
        if project.get("id") == project_id:
            return project
    return None

def apply_to_project(project_id: int, applicant_id: str) -> Optional[Dict]:

    projects = load_projects()
    
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
            for app in project.get("applications", []):
                if app.get("user_id") == applicant_id:
                    return project
            
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

def hire_freelancer(project_id: int, freelancer_id: str, escrow_app_id: int, freelancer_wallet: str) -> Optional[Dict]:

    projects = load_projects()
    
    for i, project in enumerate(projects):
        if project.get("id") == project_id:
            project["status"] = "in_progress"
            project["hired_freelancer_id"] = freelancer_id
            project["hired_freelancer_wallet"] = freelancer_wallet
            project["escrow_app_id"] = escrow_app_id
            project["hired_at"] = datetime.utcnow().isoformat()
            
            projects[i] = project
            save_projects(projects)
            
            create_notification(NotificationCreate(
                user_id=freelancer_id,
                title="Congratulations! You've been hired!",
                message=f"You've been selected for: {project.get('title')}. The escrow has been funded.",
                type="hired",
                related_id=str(project_id)
            ))
            
            return project
    
    return None

NOTIFICATIONS_DB_FILE = Path(__file__).parent.parent.parent / "data" / "notifications.json"

def ensure_notifications_db_exists():

    NOTIFICATIONS_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not NOTIFICATIONS_DB_FILE.exists():
        NOTIFICATIONS_DB_FILE.write_text(json.dumps({"notifications": []}))

def load_notifications() -> List[Dict]:

    ensure_notifications_db_exists()
    with open(NOTIFICATIONS_DB_FILE, 'r') as f:
        data = json.load(f)
    return data.get("notifications", [])

def save_notifications(notifications: List[Dict]):

    ensure_notifications_db_exists()
    with open(NOTIFICATIONS_DB_FILE, 'w') as f:
        json.dump({"notifications": notifications}, f, indent=2, default=str)

def create_notification(notification_data: NotificationCreate) -> Notification:

    notifications = load_notifications()
    
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

    notifications = load_notifications()
    user_notifications = [n for n in notifications if n.get("user_id") == user_id]
    
    user_notifications.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return [Notification(**n) for n in user_notifications]

def mark_notification_read(notification_id: str) -> Optional[Notification]:

    notifications = load_notifications()
    
    for i, notif_data in enumerate(notifications):
        if notif_data.get("id") == notification_id:
            notif_data["is_read"] = True
            notifications[i] = notif_data
            save_notifications(notifications)
            return Notification(**notif_data)
            
    return None

def get_unread_count(user_id: str) -> int:

    notifications = load_notifications()
    return sum(1 for n in notifications if n.get("user_id") == user_id and not n.get("is_read"))

MARKETPLACE_DB_FILE = Path(__file__).parent.parent.parent / "data" / "marketplace.json"

def ensure_marketplace_db_exists():

    MARKETPLACE_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not MARKETPLACE_DB_FILE.exists():
        MARKETPLACE_DB_FILE.write_text(json.dumps({"listings": []}))

def load_listings() -> List[Dict]:

    ensure_marketplace_db_exists()
    with open(MARKETPLACE_DB_FILE, 'r') as f:
        data = json.load(f)
    return data.get("listings", [])

def save_listings(listings: List[Dict]):

    ensure_marketplace_db_exists()
    with open(MARKETPLACE_DB_FILE, 'w') as f:
        json.dump({"listings": listings}, f, indent=2, default=str)

def get_all_listings() -> List[Dict]:

    return load_listings()

def create_listing(listing_data: Dict) -> Dict:

    listings = load_listings()
    
    listing_id = len(listings) + 1
    
    new_listing = {
        "id": listing_id,
        "title": listing_data.get("title"),
        "description": listing_data.get("description"),
        "category": listing_data.get("category"),
        "price_algo": listing_data.get("price_algo"),
        "condition": listing_data.get("condition"),
        "ipfs_cid": listing_data.get("ipfs_cid", ""),
        "seller_address": listing_data.get("seller_address"),
        "status": "available",
        "created_at": datetime.utcnow().isoformat(),
    }
    
    listings.append(new_listing)
    save_listings(listings)
    
    return new_listing

def update_listing_status(listing_id: int, status: str) -> Optional[Dict]:

    listings = load_listings()
    
    for i, listing in enumerate(listings):
        if listing.get("id") == listing_id:
            listing["status"] = status
            listings[i] = listing
            save_listings(listings)
            return listing
            
    return None
