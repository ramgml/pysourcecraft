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

    async def _get(self, path: str, **kwargs):
        """Make GET request."""
        return await self._client.get(path, **kwargs)

    async def _post(self, path: str, **kwargs):
        """Make POST request."""
        return await self._client.post(path, **kwargs)

    async def _patch(self, path: str, **kwargs):
        """Make PATCH request."""
        return await self._client.patch(path, **kwargs)

    async def _delete(self, path: str, **kwargs):
        """Make DELETE request."""
        return await self._client.delete(path, **kwargs)

    def _paginated_params(
        self, params: dict | None = None, page: int = 1, per_page: int = 30
    ) -> dict:
        """Build pagination parameters."""
        result = params.copy() if params else {}
        result["page"] = page
        result["per_page"] = per_page
        return result
