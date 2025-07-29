from typing import Dict, Optional

from .api.emails import Emails
from .api.contacts import Contacts
from .api.webhooks import Webhooks
from .utils.http_client import HttpClient
from .interfaces.types import SmashSendClientOptions
from .errors import AuthenticationError


class SmashSend:
    """
    SmashSend API client for Python
    """

    def __init__(self, api_key: str, options: Optional[SmashSendClientOptions] = None):
        """
        Create a new SmashSend client instance

        Args:
            api_key: Your SmashSend API key
            options: Configuration options for the client
        """
        if not api_key:
            raise AuthenticationError("API key is required", code="api_key_required")

        options = options or {}
        
        # Initialize the HTTP client
        self._http_client = HttpClient(
            api_key=api_key,
            base_url=options.get("base_url", "https://api.smashsend.com"),
            max_retries=options.get("max_retries", 3),
            timeout=options.get("timeout", 30000),
            api_version=options.get("api_version", "v1")
        )

        # Initialize API resources
        self.emails = Emails(self._http_client)
        self.contacts = Contacts(self._http_client)
        self.webhooks = Webhooks(self._http_client)

    def set_headers(self, headers: Dict[str, str]) -> "SmashSend":
        """
        Set custom headers to be included with every request

        Args:
            headers: Dictionary of header names and values

        Returns:
            The SmashSend instance for chaining
        """
        self._http_client.set_headers(headers)
        return self

    def set_header(self, name: str, value: str) -> "SmashSend":
        """
        Set a specific custom header

        Args:
            name: Header name
            value: Header value

        Returns:
            The SmashSend instance for chaining
        """
        self._http_client.set_header(name, value)
        return self

    def set_debug_mode(self, enabled: bool) -> "SmashSend":
        """
        Enable or disable debug mode
        When enabled, requests and responses will be logged

        Args:
            enabled: Whether debug mode should be enabled

        Returns:
            The SmashSend instance for chaining
        """
        self._http_client.set_debug_mode(enabled)
        return self

    def set_api_version(self, version: str) -> "SmashSend":
        """
        Set the API version to use for requests

        Args:
            version: API version string (e.g., 'v1', 'v2', etc.)

        Returns:
            The SmashSend instance for chaining
        """
        self._http_client.set_api_version(version)
        return self 