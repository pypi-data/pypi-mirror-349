from typing import Dict, List, Optional

from ..interfaces.types import Contact, ContactCreateOptions
from ..utils.http_client import HttpClient


class Contacts:
    """
    Contacts API resource
    """

    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

    def create(self, options: ContactCreateOptions) -> Contact:
        """
        Create a contact

        Args:
            options: Contact create options

        Returns:
            Created contact

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        response = self._http_client.request(
            method="POST",
            path="/contacts",
            data=options.model_dump(),
        )
        return Contact(**response)

    def get(self, contact_id: str) -> Contact:
        """
        Get contact details

        Args:
            contact_id: Contact ID

        Returns:
            Contact details

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        response = self._http_client.request(
            method="GET",
            path=f"/contacts/{contact_id}",
        )
        return Contact(**response)

    def update(self, contact_id: str, options: ContactCreateOptions) -> Contact:
        """
        Update a contact

        Args:
            contact_id: Contact ID
            options: Contact update options

        Returns:
            Updated contact

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        response = self._http_client.request(
            method="PUT",
            path=f"/contacts/{contact_id}",
            data=options.model_dump(),
        )
        return Contact(**response)

    def delete(self, contact_id: str) -> None:
        """
        Delete a contact

        Args:
            contact_id: Contact ID

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        self._http_client.request(
            method="DELETE",
            path=f"/contacts/{contact_id}",
        )

    def list(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> Dict[str, List[Contact]]:
        """
        List contacts

        Args:
            limit: Number of contacts to return
            offset: Number of contacts to skip

        Returns:
            List of contacts with pagination info

        Raises:
            APIError: If the API returns an error response
            NetworkError: If there's a network error
            TimeoutError: If the request times out
        """
        params = {
            "limit": limit,
            "offset": offset,
        }

        response = self._http_client.request(
            method="GET",
            path="/contacts",
            params=params,
        )
        return {
            "contacts": [Contact(**item) for item in response["contacts"]],
            "pagination": response["pagination"],
        } 