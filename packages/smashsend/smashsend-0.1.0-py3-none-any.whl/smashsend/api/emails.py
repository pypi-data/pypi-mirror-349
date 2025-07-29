from typing import Dict, List, Optional

from ..interfaces.types import EmailSendOptions, EmailSendResponse
from ..utils.http_client import HttpClient


class Emails:
    """
    Emails API resource
    """

    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

    def send(self, options: EmailSendOptions) -> EmailSendResponse:
        """
        Send an email

        Args:
            options: Email send options

        Returns:
            Email send response

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        response = self._http_client.request(
            method="POST",
            path="/emails",
            data=options.model_dump(by_alias=True),
        )
        return EmailSendResponse(**response)

    def get(self, email_id: str) -> EmailSendResponse:
        """
        Get email details

        Args:
            email_id: Email ID

        Returns:
            Email details

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        response = self._http_client.request(
            method="GET",
            path=f"/emails/{email_id}",
        )
        return EmailSendResponse(**response)

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        status: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, List[EmailSendResponse]]:
        """
        List emails

        Args:
            page: Page number
            per_page: Items per page
            status: Filter by status
            tag: Filter by tag

        Returns:
            List of emails

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        params = {
            "page": page,
            "per_page": per_page,
        }
        if status:
            params["status"] = status
        if tag:
            params["tag"] = tag

        response = self._http_client.request(
            method="GET",
            path="/emails",
            params=params,
        )
        return {
            "data": [EmailSendResponse(**item) for item in response["data"]],
            "total": response["total"],
            "page": response["page"],
            "per_page": response["per_page"],
        } 