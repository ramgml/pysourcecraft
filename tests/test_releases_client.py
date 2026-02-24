"""Integration tests for the ReleasesClient."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import (
    CreateReleaseRequest,
    PaginatedResponse,
    Release,
    ReleaseAsset,
    ReleaseState,
    UpdateReleaseRequest,
)

from tests.conftest import create_paginated_response


class TestReleasesClientList:
    """Tests for listing releases."""

    @pytest.mark.asyncio
    async def test_list_releases(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_release_data: dict[str, Any],
    ) -> None:
        """Test listing releases."""
        response_data = create_paginated_response([mock_release_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.releases.list("testuser", "test-repo")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.total == 1

    @pytest.mark.asyncio
    async def test_list_releases_pagination(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_release_data: dict[str, Any],
    ) -> None:
        """Test listing releases with pagination."""
        response_data = create_paginated_response(
            [mock_release_data], page=1, per_page=10, total=5
        )
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.releases.list("testuser", "test-repo", per_page=10)

        assert result.per_page == 10
        assert result.total == 5


class TestReleasesClientGet:
    """Tests for getting a single release."""

    @pytest.mark.asyncio
    async def test_get_release_by_id(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_release_data: dict[str, Any],
    ) -> None:
        """Test getting a release by ID."""
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/release-001"
        ).mock(return_value=Response(200, json=mock_release_data))

        result = await client.releases.get("testuser", "test-repo", "release-001")

        assert isinstance(result, Release)
        assert result.id == "release-001"
        assert result.tag_name == "v1.0.0"
        assert result.name == "Version 1.0.0"

    @pytest.mark.asyncio
    async def test_get_release_by_tag(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_release_data: dict[str, Any],
    ) -> None:
        """Test getting a release by tag."""
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/tags/v1.0.0"
        ).mock(return_value=Response(200, json=mock_release_data))

        result = await client.releases.get_by_tag("testuser", "test-repo", "v1.0.0")

        assert isinstance(result, Release)
        assert result.tag_name == "v1.0.0"

    @pytest.mark.asyncio
    async def test_get_latest_release(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_release_data: dict[str, Any],
    ) -> None:
        """Test getting the latest release."""
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/latest"
        ).mock(return_value=Response(200, json=mock_release_data))

        result = await client.releases.get_latest("testuser", "test-repo")

        assert isinstance(result, Release)
        assert result.tag_name == "v1.0.0"


class TestReleasesClientCreate:
    """Tests for creating releases."""

    @pytest.mark.asyncio
    async def test_create_release(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_release_data: dict[str, Any],
    ) -> None:
        """Test creating a new release."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases"
        ).mock(return_value=Response(201, json=mock_release_data))

        request = CreateReleaseRequest(
            tag_name="v1.0.0",
            name="Version 1.0.0",
            body="Initial release",
        )
        result = await client.releases.create("testuser", "test-repo", request)

        assert isinstance(result, Release)
        assert result.tag_name == "v1.0.0"

    @pytest.mark.asyncio
    async def test_create_draft_release(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_release_data: dict[str, Any],
    ) -> None:
        """Test creating a draft release."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases"
        ).mock(return_value=Response(201, json=mock_release_data))

        request = CreateReleaseRequest(
            tag_name="v2.0.0",
            name="Version 2.0.0",
            draft=True,
        )
        result = await client.releases.create("testuser", "test-repo", request)

        assert isinstance(result, Release)

    @pytest.mark.asyncio
    async def test_create_prerelease(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_release_data: dict[str, Any],
    ) -> None:
        """Test creating a prerelease."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases"
        ).mock(return_value=Response(201, json=mock_release_data))

        request = CreateReleaseRequest(
            tag_name="v2.0.0-beta",
            name="Version 2.0.0 Beta",
            prerelease=True,
        )
        result = await client.releases.create("testuser", "test-repo", request)

        assert isinstance(result, Release)


class TestReleasesClientUpdate:
    """Tests for updating releases."""

    @pytest.mark.asyncio
    async def test_update_release(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_release_data: dict[str, Any],
    ) -> None:
        """Test updating a release."""
        mock_router.patch(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/release-001"
        ).mock(return_value=Response(200, json=mock_release_data))

        request = UpdateReleaseRequest(name="Updated Release Name")
        result = await client.releases.update(
            "testuser", "test-repo", "release-001", request
        )

        assert isinstance(result, Release)


class TestReleasesClientDelete:
    """Tests for deleting releases."""

    @pytest.mark.asyncio
    async def test_delete_release(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test deleting a release."""
        mock_router.delete(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/release-001"
        ).mock(return_value=Response(204, json={}))

        result = await client.releases.delete("testuser", "test-repo", "release-001")

        assert result is None


class TestReleasesClientAssets:
    """Tests for release assets."""

    @pytest.mark.asyncio
    async def test_list_assets(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test listing assets for a release."""
        asset_data = {
            "id": "asset-001",
            "name": "app-v1.0.0.zip",
            "content_type": "application/zip",
            "size": 1024000,
            "download_count": 100,
            "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/assets/1",
            "browser_download_url": "https://sourcecraft.dev/testuser/test-repo/releases/download/v1.0.0/app-v1.0.0.zip",
            "created_at": mock_datetime.isoformat(),
            "updated_at": mock_datetime.isoformat(),
        }
        response_data = create_paginated_response([asset_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/release-001/assets"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.releases.list_assets(
            "testuser", "test-repo", "release-001"
        )

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].name == "app-v1.0.0.zip"

    @pytest.mark.asyncio
    async def test_upload_asset(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test uploading an asset to a release."""
        asset_data = {
            "id": "asset-002",
            "name": "release-notes.md",
            "content_type": "text/markdown",
            "size": 1024,
            "download_count": 0,
            "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/assets/2",
            "browser_download_url": "https://sourcecraft.dev/testuser/test-repo/releases/download/v1.0.0/release-notes.md",
            "created_at": mock_datetime.isoformat(),
            "updated_at": mock_datetime.isoformat(),
        }
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/release-001/assets"
        ).mock(return_value=Response(201, json=asset_data))

        content = b"# Release Notes\n\nThis is a test release."
        result = await client.releases.upload_asset(
            "testuser",
            "test-repo",
            "release-001",
            "release-notes.md",
            content,
            "text/markdown",
        )

        assert isinstance(result, ReleaseAsset)
        assert result.name == "release-notes.md"
        assert result.content_type == "text/markdown"

    @pytest.mark.asyncio
    async def test_delete_asset(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test deleting a release asset."""
        mock_router.delete(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/assets/asset-001"
        ).mock(return_value=Response(204, json={}))

        result = await client.releases.delete_asset(
            "testuser", "test-repo", "asset-001"
        )

        assert result is None
