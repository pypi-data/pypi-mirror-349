from .client import SmashSend
from .errors import (
    SmashSendError,
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    TimeoutError,
)
from .interfaces.types import (
    SmashSendClientOptions,
    EmailSendOptions,
    EmailSendResponse,
    ContactCreateOptions,
    Contact,
    WebhookCreateOptions,
    Webhook,
    EmailAddress,
    EmailAttachment,
    SmashsendContactStatus,
    SmashsendCountryCode,
)

__version__ = "0.1.0"

__all__ = [
    "SmashSend",
    "SmashSendError",
    "APIError",
    "AuthenticationError",
    "NetworkError",
    "RateLimitError",
    "TimeoutError",
    "SmashSendClientOptions",
    "EmailSendOptions",
    "EmailSendResponse",
    "ContactCreateOptions",
    "Contact",
    "WebhookCreateOptions",
    "Webhook",
    "EmailAddress",
    "EmailAttachment",
    "SmashsendContactStatus",
    "SmashsendCountryCode",
] 