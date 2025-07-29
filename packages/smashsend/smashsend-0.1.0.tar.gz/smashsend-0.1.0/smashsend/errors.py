from typing import Any, Dict, Optional


class SmashSendError(Exception):
    """Base exception class for all SmashSend errors"""

    def __init__(self, message: str, code: str = "unknown_error", details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class APIError(SmashSendError):
    """Raised when the API returns an error response"""

    def __init__(
        self,
        message: str,
        code: str = "api_error",
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, code, details)
        self.status_code = status_code


class AuthenticationError(SmashSendError):
    """Raised when there's an authentication error"""

    def __init__(
        self,
        message: str,
        code: str = "authentication_error",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, code, details)


class NetworkError(SmashSendError):
    """Raised when there's a network error"""

    def __init__(
        self,
        message: str,
        code: str = "network_error",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, code, details)


class RateLimitError(SmashSendError):
    """Raised when the API rate limit is exceeded"""

    def __init__(
        self,
        message: str,
        code: str = "rate_limit_error",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, code, details)


class TimeoutError(SmashSendError):
    """Raised when a request times out"""

    def __init__(
        self,
        message: str,
        code: str = "timeout_error",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, code, details) 