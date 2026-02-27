from typing import Optional
from pydantic import BaseModel

class Notification(BaseModel):

    id: str
    user_id: str
    title: str
    message: str
    type: str
    related_id: Optional[str] = None
    is_read: bool = False
    created_at: str

class NotificationCreate(BaseModel):

    user_id: str
    title: str
    message: str
    type: str
    related_id: Optional[str] = None
