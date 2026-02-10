"""
CampusNexus - Notifications Router
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query

from app.models.notification import Notification
from app.utils.database import (
    get_user_notifications,
    mark_notification_read,
    get_unread_count
)

router = APIRouter()


@router.get("/", response_model=List[Notification])
async def get_notifications(
    user_id: str = Query(..., description="ID of the user to fetch notifications for")
):
    """
    Get all notifications for a specific user.
    """
    return get_user_notifications(user_id)


@router.get("/unread-count")
async def get_unread_notification_count(
    user_id: str = Query(..., description="ID of the user")
):
    """
    Get the count of unread notifications.
    """
    count = get_unread_count(user_id)
    return {"count": count}


@router.put("/{notification_id}/read", response_model=Notification)
async def read_notification(notification_id: str):
    """
    Mark a notification as read.
    """
    notification = mark_notification_read(notification_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return notification
