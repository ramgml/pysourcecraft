"""SourceCraft API Client."""

from __future__ import annotations

import httpx

from pysourcecraft.clients import (
    CICDClient,
    IssuesClient,
    OrganizationsClient,
    PullRequestsClient,
    ReleasesClient,
    RepositoriesClient,
    UsersClient,
)
from pysourcecraft.models import APIError, ErrorResponse


class SourceCraftClient:
    """Async HTTP client for SourceCraft API."""

    def __init__(
        self,
        api_token: str | None = None,
        base_url: str = "https://api.sourcecraft.tech",
        timeout: float = 30.0,
    ):
        """Initialize the client.

        Args:
            api_token: API token for authentication
            base_url: Base URL for the API
            timeout: Request timeout in seconds
        """
        self.api_token = api_token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

        # Resource clients
        self.issues = IssuesClient(self)
        self.pull_requests = PullRequestsClient(self)
        self.repositories = RepositoriesClient(self)
        self.releases = ReleasesClient(self)
        self.users = UsersClient(self)
        self.organizations = OrganizationsClient(self)
        self.cicd = CICDClient(self)

    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create httpx client."""
        if self._client is None or self._client.is_closed:
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=headers,
            )
        return self._client

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> dict:
        """Make an HTTP request.

        Args:
            method: HTTP method
            path: API path
            **kwargs: Additional arguments for httpx

        Returns:
            JSON response as dictionary

        Raises:
            APIError: If the request fails
        """
        try:
            response = await self.client.request(method, path, **kwargs)
            response.raise_for_status()

            # Validate Content-Type before parsing JSON
            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type:
                body_preview = response.text[:500]
                raise APIError(
                    message=(
                        f"Expected JSON response, but received '{content_type}'. "
                        f"HTTP {response.status_code}: {body_preview}"
                    ),
                    status_code=response.status_code,
                )

            return response.json()
        except httpx.HTTPStatusError as e:
            error_response = None
            try:
                error_data = e.response.json()
                error_response = ErrorResponse.model_validate(error_data)
            except Exception:
                pass
            raise APIError(
                message=str(e),
                status_code=e.response.status_code,
                error_response=error_response,
            ) from e
        except httpx.HTTPError as e:
            raise APIError(message=str(e)) from e

    async def get(self, path: str, **kwargs) -> dict:
        """Make a GET request."""
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> dict:
        """Make a POST request."""
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs) -> dict:
        """Make a PUT request."""
        return await self._request("PUT", path, **kwargs)

    async def patch(self, path: str, **kwargs) -> dict:
        """Make a PATCH request."""
        return await self._request("PATCH", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> dict:
        """Make a DELETE request."""
        return await self._request("DELETE", path, **kwargs)

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def __aenter__(self) -> SourceCraftClient:
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args) -> None:
        """Async context manager exit."""
        await self.close()
