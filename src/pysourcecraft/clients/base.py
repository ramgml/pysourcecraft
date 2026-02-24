"""Base client for SourceCraft API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar


if TYPE_CHECKING:
    from pysourcecraft.client import SourceCraftClient

T = TypeVar("T")


class BaseResourceClient:
    """Base class for resource-specific clients."""

    def __init__(self, client: SourceCraftClient):
        """Initialize with parent client.

        Args:
            client: The main SourceCraftClient instance
        """
        self._client = client

    async def _get(self, path: str, **kwargs) -> dict:
        """Make a GET request to the SourceCraft API.

        Args:
            path: API endpoint path (relative to base URL)
            **kwargs: Additional arguments passed to httpx request

        Returns:
            JSON response as dictionary

        Raises:
            APIError: If the request fails with an HTTP error
        """
        return await self._client.get(path, **kwargs)

    async def _post(self, path: str, **kwargs) -> dict:
        """Make a POST request to the SourceCraft API.

        Args:
            path: API endpoint path (relative to base URL)
            **kwargs: Additional arguments passed to httpx request

        Returns:
            JSON response as dictionary

        Raises:
            APIError: If the request fails with an HTTP error
        """
        return await self._client.post(path, **kwargs)

    async def _patch(self, path: str, **kwargs) -> dict:
        """Make a PATCH request to the SourceCraft API.

        Args:
            path: API endpoint path (relative to base URL)
            **kwargs: Additional arguments passed to httpx request

        Returns:
            JSON response as dictionary

        Raises:
            APIError: If the request fails with an HTTP error
        """
        return await self._client.patch(path, **kwargs)

    async def _delete(self, path: str, **kwargs) -> dict:
        """Make a DELETE request to the SourceCraft API.

        Args:
            path: API endpoint path (relative to base URL)
            **kwargs: Additional arguments passed to httpx request

        Returns:
            JSON response as dictionary (may be empty for successful deletions)

        Raises:
            APIError: If the request fails with an HTTP error
        """
        return await self._client.delete(path, **kwargs)

    def _paginated_params(
        self, params: dict | None = None, page: int = 1, per_page: int = 30
    ) -> dict:
        """Build pagination parameters for API requests.

        Args:
            params: Existing parameters dictionary to extend (optional)
            page: Page number (1-indexed, default: 1)
            per_page: Number of items per page (default: 30, max: 100)

        Returns:
            Dictionary containing pagination parameters
        """
        result = params.copy() if params else {}
        result["page"] = page
        result["per_page"] = per_page
        return result
