"""Integration tests for the SourceCraftClient."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
import respx
from httpx import Response

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import APIError, ErrorDetail, ErrorResponse


class TestClientInitialization:
    """Tests for client initialization."""

    def test_client_init_with_token(self) -> None:
        """Test client initialization with API token."""
        client = SourceCraftClient(api_token="test-token")

        assert client.api_token == "test-token"
        assert client.base_url == "https://api.sourcecraft.tech"
        assert client.timeout == 30.0
        assert client._client is None

    def test_client_init_without_token(self) -> None:
        """Test client initialization without API token."""
        client = SourceCraftClient(api_token=None)

        assert client.api_token is None
        assert client.base_url == "https://api.sourcecraft.tech"

    def test_client_init_custom_base_url(self) -> None:
        """Test client initialization with custom base URL."""
        client = SourceCraftClient(
            api_token="test-token",
            base_url="https://custom.api.com/v2/",
        )

        assert client.base_url == "https://custom.api.com/v2"

    def test_client_init_custom_timeout(self) -> None:
        """Test client initialization with custom timeout."""
        client = SourceCraftClient(api_token="test-token", timeout=60.0)

        assert client.timeout == 60.0


class TestClientHTTPClient:
    """Tests for HTTP client creation."""

    def test_client_lazy_initialization(self) -> None:
        """Test that HTTP client is created lazily."""
        client = SourceCraftClient(api_token="test-token")
        assert client._client is None

        # Accessing the client property creates it
        http_client = client.client
        assert http_client is not None
        assert isinstance(http_client, httpx.AsyncClient)

    def test_client_headers_with_token(self) -> None:
        """Test that headers include authorization when token is provided."""
        client = SourceCraftClient(api_token="test-token")
        http_client = client.client

        assert http_client.headers["Authorization"] == "Bearer test-token"
        assert http_client.headers["Accept"] == "application/json"
        assert http_client.headers["Content-Type"] == "application/json"

    def test_client_headers_without_token(self) -> None:
        """Test that headers don't include authorization when no token."""
        client = SourceCraftClient(api_token=None)
        http_client = client.client

        assert "Authorization" not in http_client.headers
        assert http_client.headers["Accept"] == "application/json"

    @pytest.mark.asyncio
    async def test_client_close(self) -> None:
        """Test closing the client."""
        client = SourceCraftClient(api_token="test-token")
        # Initialize the client
        _ = client.client

        await client.close()
        assert client._client is not None
        assert client._client.is_closed

    @pytest.mark.asyncio
    async def test_client_context_manager(self) -> None:
        """Test using client as async context manager."""
        async with SourceCraftClient(api_token="test-token") as client:
            assert isinstance(client, SourceCraftClient)
            assert client.api_token == "test-token"


class TestClientHTTPMethods:
    """Tests for HTTP request methods."""

    @pytest.mark.asyncio
    async def test_get_request(
        self, client: SourceCraftClient, mock_router: respx.MockRouter
    ) -> None:
        """Test GET request."""
        mock_router.get("https://api.sourcecraft.dev/v1/test").mock(
            return_value=Response(200, json={"message": "success"})
        )

        result = await client.get("/test")

        assert result == {"message": "success"}

    @pytest.mark.asyncio
    async def test_post_request(
        self, client: SourceCraftClient, mock_router: respx.MockRouter
    ) -> None:
        """Test POST request."""
        mock_router.post("https://api.sourcecraft.dev/v1/test").mock(
            return_value=Response(201, json={"id": "123", "message": "created"})
        )

        result = await client.post("/test", json={"name": "test"})

        assert result["id"] == "123"
        assert result["message"] == "created"

    @pytest.mark.asyncio
    async def test_put_request(
        self, client: SourceCraftClient, mock_router: respx.MockRouter
    ) -> None:
        """Test PUT request."""
        mock_router.put("https://api.sourcecraft.dev/v1/test/123").mock(
            return_value=Response(200, json={"id": "123", "updated": True})
        )

        result = await client.put("/test/123", json={"name": "updated"})

        assert result["updated"] is True

    @pytest.mark.asyncio
    async def test_patch_request(
        self, client: SourceCraftClient, mock_router: respx.MockRouter
    ) -> None:
        """Test PATCH request."""
        mock_router.patch("https://api.sourcecraft.dev/v1/test/123").mock(
            return_value=Response(200, json={"id": "123", "patched": True})
        )

        result = await client.patch("/test/123", json={"field": "value"})

        assert result["patched"] is True

    @pytest.mark.asyncio
    async def test_delete_request(
        self, client: SourceCraftClient, mock_router: respx.MockRouter
    ) -> None:
        """Test DELETE request."""
        mock_router.delete("https://api.sourcecraft.dev/v1/test/123").mock(
            return_value=Response(204, json={})
        )

        result = await client.delete("/test/123")

        assert result == {}


class TestClientErrorHandling:
    """Tests for error handling."""

    @pytest.mark.asyncio
    async def test_http_status_error_with_json(
        self, client: SourceCraftClient, mock_router: respx.MockRouter
    ) -> None:
        """Test handling HTTP error with JSON error response."""
        error_data = {
            "error": "NotFound",
            "message": "Resource not found",
            "details": [{"field": "id", "message": "Invalid ID", "code": "invalid"}],
            "status_code": 404,
        }
        mock_router.get("https://api.sourcecraft.dev/v1/notfound").mock(
            return_value=Response(404, json=error_data)
        )

        with pytest.raises(APIError) as exc_info:
            await client.get("/notfound")

        error = exc_info.value
        assert error.status_code == 404
        assert error.error_response is not None
        assert error.error_response.error == "NotFound"
        assert error.error_response.message == "Resource not found"
        assert len(error.error_response.details) == 1
        assert error.error_response.details[0].field == "id"

    @pytest.mark.asyncio
    async def test_http_status_error_without_json(
        self, client: SourceCraftClient, mock_router: respx.MockRouter
    ) -> None:
        """Test handling HTTP error without JSON response."""
        mock_router.get("https://api.sourcecraft.dev/v1/server-error").mock(
            return_value=Response(500, text="Internal Server Error")
        )

        with pytest.raises(APIError) as exc_info:
            await client.get("/server-error")

        error = exc_info.value
        assert error.status_code == 500
        assert error.error_response is None

    @pytest.mark.asyncio
    async def test_http_connection_error(
        self, client: SourceCraftClient, mock_router: respx.MockRouter
    ) -> None:
        """Test handling HTTP connection error."""
        mock_router.get("https://api.sourcecraft.dev/v1/connection-error").mock(
            side_effect=httpx.ConnectError("Connection failed")
        )

        with pytest.raises(APIError) as exc_info:
            await client.get("/connection-error")

        error = exc_info.value
        assert "Connection failed" in error.message
        assert error.status_code is None

    @pytest.mark.asyncio
    async def test_http_timeout_error(
        self, client: SourceCraftClient, mock_router: respx.MockRouter
    ) -> None:
        """Test handling HTTP timeout error."""
        mock_router.get("https://api.sourcecraft.dev/v1/timeout").mock(
            side_effect=httpx.TimeoutException("Request timed out")
        )

        with pytest.raises(APIError) as exc_info:
            await client.get("/timeout")

        error = exc_info.value
        assert "timed out" in error.message


class TestClientErrorDetails:
    """Tests for APIError exception."""

    def test_api_error_str_with_status_code(self) -> None:
        """Test APIError string representation with status code."""
        error = APIError(message="Something went wrong", status_code=500)
        assert str(error) == "[500] Something went wrong"

    def test_api_error_str_without_status_code(self) -> None:
        """Test APIError string representation without status code."""
        error = APIError(message="Connection failed")
        assert str(error) == "Connection failed"

    def test_api_error_with_error_response(self) -> None:
        """Test APIError with full error response."""
        error_response = ErrorResponse(
            error="ValidationError",
            message="Invalid input",
            status_code=422,
            details=[
                ErrorDetail(field="email", message="Invalid email", code="invalid")
            ],
        )
        error = APIError(
            message="Validation failed",
            status_code=422,
            error_response=error_response,
        )

        assert error.error_response == error_response
        assert error.error_response is not None
        assert error.error_response.error == "ValidationError"


class TestClientResourceClients:
    """Tests for resource client accessors."""

    def test_issues_client(self) -> None:
        """Test issues client is accessible."""
        client = SourceCraftClient(api_token="test-token")
        from pysourcecraft.clients import IssuesClient

        assert isinstance(client.issues, IssuesClient)
        assert client.issues._client is client

    def test_pull_requests_client(self) -> None:
        """Test pull requests client is accessible."""
        client = SourceCraftClient(api_token="test-token")
        from pysourcecraft.clients import PullRequestsClient

        assert isinstance(client.pull_requests, PullRequestsClient)

    def test_repositories_client(self) -> None:
        """Test repositories client is accessible."""
        client = SourceCraftClient(api_token="test-token")
        from pysourcecraft.clients import RepositoriesClient

        assert isinstance(client.repositories, RepositoriesClient)

    def test_releases_client(self) -> None:
        """Test releases client is accessible."""
        client = SourceCraftClient(api_token="test-token")
        from pysourcecraft.clients import ReleasesClient

        assert isinstance(client.releases, ReleasesClient)

    def test_users_client(self) -> None:
        """Test users client is accessible."""
        client = SourceCraftClient(api_token="test-token")
        from pysourcecraft.clients import UsersClient

        assert isinstance(client.users, UsersClient)

    def test_organizations_client(self) -> None:
        """Test organizations client is accessible."""
        client = SourceCraftClient(api_token="test-token")
        from pysourcecraft.clients import OrganizationsClient

        assert isinstance(client.organizations, OrganizationsClient)

    def test_cicd_client(self) -> None:
        """Test CI/CD client is accessible."""
        client = SourceCraftClient(api_token="test-token")
        from pysourcecraft.clients import CICDClient

        assert isinstance(client.cicd, CICDClient)
