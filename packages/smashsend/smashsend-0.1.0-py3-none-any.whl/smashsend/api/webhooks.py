from typing import Dict, List, Optional

from ..interfaces.types import Webhook, WebhookCreateOptions
from ..utils.http_client import HttpClient


class Webhooks:
    """
    Webhooks API resource
    """

    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

    def create(self, options: WebhookCreateOptions) -> Webhook:
        """
        Create a webhook

        Args:
            options: Webhook create options

        Returns:
            Created webhook

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        response = self._http_client.request(
            method="POST",
            path="/webhooks",
            data=options.model_dump(),
        )
        return Webhook(**response)

    def get(self, webhook_id: str) -> Webhook:
        """
        Get webhook details

        Args:
            webhook_id: Webhook ID

        Returns:
            Webhook details

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        response = self._http_client.request(
            method="GET",
            path=f"/webhooks/{webhook_id}",
        )
        return Webhook(**response)

    def update(self, webhook_id: str, options: WebhookCreateOptions) -> Webhook:
        """
        Update a webhook

        Args:
            webhook_id: Webhook ID
            options: Webhook update options

        Returns:
            Updated webhook

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        response = self._http_client.request(
            method="PUT",
            path=f"/webhooks/{webhook_id}",
            data=options.model_dump(),
        )
        return Webhook(**response)

    def delete(self, webhook_id: str) -> None:
        """
        Delete a webhook

        Args:
            webhook_id: Webhook ID

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        self._http_client.request(
            method="DELETE",
            path=f"/webhooks/{webhook_id}",
        )

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        status: Optional[str] = None,
    ) -> Dict[str, List[Webhook]]:
        """
        List webhooks

        Args:
            page: Page number
            per_page: Items per page
            status: Filter by status

        Returns:
            List of webhooks

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

        response = self._http_client.request(
            method="GET",
            path="/webhooks",
            params=params,
        )
        return {
            "data": [Webhook(**item) for item in response["data"]],
            "total": response["total"],
            "page": response["page"],
            "per_page": response["per_page"],
        } 