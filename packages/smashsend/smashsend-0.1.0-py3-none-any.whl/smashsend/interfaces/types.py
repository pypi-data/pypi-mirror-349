from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class SmashsendContactStatus(str, Enum):
    """Contact status enum"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNSUBSCRIBED = "unsubscribed"


class SmashsendCountryCode(str, Enum):
    """Country code enum"""
    US = "US"
    CA = "CA"
    GB = "GB"
    # Add more country codes as needed


class EmailAddress(BaseModel):
    """Email address model"""
    email: str
    name: Optional[str] = None


class EmailAttachment(BaseModel):
    """Email attachment model"""
    filename: str
    content: str  # Base64 encoded content
    content_type: Optional[str] = None


class EmailSendOptions(BaseModel):
    """Email send options model"""
    to: List[EmailAddress]
    from_: EmailAddress = Field(..., alias="from")
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None
    cc: Optional[List[EmailAddress]] = None
    bcc: Optional[List[EmailAddress]] = None
    reply_to: Optional[EmailAddress] = None
    attachments: Optional[List[EmailAttachment]] = None
    template_id: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class EmailSendResponse(BaseModel):
    """Email send response model"""
    id: str
    message_id: str
    status: str
    created_at: str


class ContactCreateOptions(BaseModel):
    """Contact create options model"""
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[SmashsendCountryCode] = None
    status: SmashsendContactStatus = SmashsendContactStatus.ACTIVE
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class Contact(BaseModel):
    """Contact model"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[SmashsendCountryCode] = None
    status: SmashsendContactStatus
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    created_at: str
    updated_at: str


class WebhookCreateOptions(BaseModel):
    """Webhook create options model"""
    url: str
    events: List[str]
    description: Optional[str] = None
    secret: Optional[str] = None


class Webhook(BaseModel):
    """Webhook model"""
    id: str
    url: str
    events: List[str]
    description: Optional[str] = None
    status: str
    created_at: str
    updated_at: str


class SmashSendClientOptions(BaseModel):
    """Client options model"""
    base_url: Optional[str] = None
    max_retries: Optional[int] = None
    timeout: Optional[int] = None
    api_version: Optional[str] = None 