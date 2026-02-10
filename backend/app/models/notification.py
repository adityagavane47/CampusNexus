"""
CampusNexus - Notification Model
"""
from typing import Optional
from pydantic import BaseModel

class Notification(BaseModel):
    """
    Represents a user notification.
    """
    id: str  # Unique ID for the notification
    user_id: str  # The recipient of the notification
    title: str
    message: str
    type: str  # e.g., 'application', 'system', 'payment'
    related_id: Optional[str] = None  # ID of related entity (e.g., project_id)
    is_read: bool = False
    created_at: str

class NotificationCreate(BaseModel):
    """
    Schema for creating a notification.
    """
    user_id: str
    title: str
    message: str
    type: str
    related_id: Optional[str] = None
