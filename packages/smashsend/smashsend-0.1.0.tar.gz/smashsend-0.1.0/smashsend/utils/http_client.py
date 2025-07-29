import json
import logging
from typing import Any, Dict, Optional, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..errors import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    TimeoutError,
)

logger = logging.getLogger(__name__)


class HttpClient:
    """
    HTTP client for making requests to the SmashSend API
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.smashsend.com",
        max_retries: int = 3,
        timeout: int = 30000,
        api_version: str = "v1",
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout / 1000  # Convert to seconds
        self.api_version = api_version
        self.debug_mode = False
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def set_headers(self, headers: Dict[str, str]) -> None:
        """Set custom headers for all requests"""
        self.headers.update(headers)

    def set_header(self, name: str, value: str) -> None:
        """Set a specific custom header"""
        self.headers[name] = value

    def set_debug_mode(self, enabled: bool) -> None:
        """Enable or disable debug mode"""
        self.debug_mode = enabled
        if enabled:
            logging.basicConfig(level=logging.DEBUG)

    def set_api_version(self, version: str) -> None:
        """Set the API version to use"""
        self.api_version = version

    def _build_url(self, path: str) -> str:
        """Build the full URL for a request"""
        return f"{self.base_url}/{self.api_version}/{path.lstrip('/')}"

    def _log_request(self, method: str, url: str, data: Optional[Dict] = None) -> None:
        """Log request details if debug mode is enabled"""
        if self.debug_mode:
            logger.debug(f"Request: {method} {url}")
            if data:
                logger.debug(f"Request data: {json.dumps(data, indent=2)}")

    def _log_response(self, response: requests.Response) -> None:
        """Log response details if debug mode is enabled"""
        if self.debug_mode:
            logger.debug(f"Response status: {response.status_code}")
            try:
                logger.debug(f"Response body: {json.dumps(response.json(), indent=2)}")
            except json.JSONDecodeError:
                logger.debug(f"Response body: {response.text}")

    def _handle_error(self, response: requests.Response) -> None:
        """Handle API error responses"""
        try:
            error_data = response.json()
        except json.JSONDecodeError:
            error_data = {"message": response.text}

        status_code = response.status_code
        error_message = error_data.get("message", "Unknown error")
        error_code = error_data.get("code", "unknown_error")

        if status_code == 401:
            raise AuthenticationError(error_message, code=error_code)
        elif status_code == 429:
            raise RateLimitError(error_message, code=error_code)
        elif status_code >= 500:
            raise NetworkError(error_message, code=error_code)
        else:
            raise APIError(error_message, code=error_code, status_code=status_code)

    def request(
        self,
        method: str,
        path: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Any:
        """
        Make an HTTP request to the API

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            data: Request body data
            params: URL query parameters

        Returns:
            Response data as Python object

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        url = self._build_url(path)
        self._log_request(method, url, data)

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=self.headers,
                timeout=self.timeout,
            )
            self._log_response(response)

            if not response.ok:
                self._handle_error(response)

            return response.json() if response.content else None

        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out", code="timeout")
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e), code="network_error") 