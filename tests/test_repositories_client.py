"""Integration tests for the RepositoriesClient."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import (
    CreateRepositoryRequest,
    ListOrganizationRepositoriesResponse,
    PaginatedResponse,
    RepoBranch,
    Repository,
    RepoVisibility,
    UpdateRepositoryRequest,
)

from tests.conftest import create_paginated_response


class TestRepositoriesClientList:
    """Tests for listing repositories."""

    @pytest.mark.asyncio
    async def test_list_repositories_for_user(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test listing repositories for a user."""
        # API returns ListOrganizationRepositoriesResponse format
        response_data = {
            "repositories": [mock_repository_data],
            "next_page_token": None,
        }
        mock_router.get("https://api.sourcecraft.dev/v1/users/testuser/repos").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.repositories.list("testuser")

        assert isinstance(result, ListOrganizationRepositoriesResponse)
        assert len(result.repositories) == 1
        assert result.next_page_token is None

    @pytest.mark.asyncio
    async def test_list_repositories_for_current_user(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test listing repositories for the authenticated user."""
        # API returns ListOrganizationRepositoriesResponse format
        response_data = {
            "repositories": [mock_repository_data],
            "next_page_token": None,
        }
        mock_router.get("https://api.sourcecraft.dev/v1/repos").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.repositories.list()

        assert isinstance(result, ListOrganizationRepositoriesResponse)
        assert len(result.repositories) == 1
        assert result.next_page_token is None

    @pytest.mark.asyncio
    async def test_list_org_repositories(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test listing organization repositories."""
        # API returns ListOrganizationRepositoriesResponse format
        response_data = {
            "repositories": [mock_repository_data],
            "next_page_token": None,
        }
        mock_router.get("https://api.sourcecraft.dev/v1/orgs/testorg/repos").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.repositories.list_org_repos("testorg")

        assert isinstance(result, ListOrganizationRepositoriesResponse)
        assert len(result.repositories) == 1
        assert result.next_page_token is None


class TestRepositoriesClientGet:
    """Tests for getting a single repository."""

    @pytest.mark.asyncio
    async def test_get_repository(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test getting a single repository."""
        mock_router.get("https://api.sourcecraft.dev/v1/repos/testuser/test-repo").mock(
            return_value=Response(200, json=mock_repository_data)
        )

        result = await client.repositories.get("testuser", "test-repo")

        assert isinstance(result, Repository)
        assert result.id == "repo-789"
        assert result.name == "test-repo"
        assert result.full_name == "testuser/test-repo"
        assert result.visibility == RepoVisibility.PUBLIC


class TestRepositoriesClientCreate:
    """Tests for creating repositories."""

    @pytest.mark.asyncio
    async def test_create_repository(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test creating a new repository."""
        mock_router.post("https://api.sourcecraft.dev/v1/repos").mock(
            return_value=Response(201, json=mock_repository_data)
        )

        request = CreateRepositoryRequest(
            name="test-repo",
            description="A test repository",
            visibility=RepoVisibility.PUBLIC,
        )
        result = await client.repositories.create(request)

        assert isinstance(result, Repository)
        assert result.name == "test-repo"

    @pytest.mark.asyncio
    async def test_create_org_repository(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test creating a repository in an organization."""
        mock_router.post("https://api.sourcecraft.dev/v1/orgs/testorg/repos").mock(
            return_value=Response(201, json=mock_repository_data)
        )

        request = CreateRepositoryRequest(name="test-repo")
        result = await client.repositories.create_org_repo("testorg", request)

        assert isinstance(result, Repository)


class TestRepositoriesClientUpdate:
    """Tests for updating repositories."""

    @pytest.mark.asyncio
    async def test_update_repository(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test updating a repository."""
        mock_router.patch(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo"
        ).mock(return_value=Response(200, json=mock_repository_data))

        request = UpdateRepositoryRequest(description="Updated description")
        result = await client.repositories.update("testuser", "test-repo", request)

        assert isinstance(result, Repository)

    @pytest.mark.asyncio
    async def test_archive_repository(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test archiving a repository."""
        mock_router.patch(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo"
        ).mock(return_value=Response(200, json=mock_repository_data))

        request = UpdateRepositoryRequest(archived=True)
        result = await client.repositories.update("testuser", "test-repo", request)

        assert isinstance(result, Repository)


class TestRepositoriesClientDelete:
    """Tests for deleting repositories."""

    @pytest.mark.asyncio
    async def test_delete_repository(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test deleting a repository."""
        mock_router.delete(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo"
        ).mock(return_value=Response(204, json={}))

        result = await client.repositories.delete("testuser", "test-repo")

        assert result is None


class TestRepositoriesClientBranches:
    """Tests for repository branches."""

    @pytest.mark.asyncio
    async def test_list_branches(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test listing branches in a repository."""
        branch_data = {
            "name": "main",
            "commit_sha": "abc123def456",
            "protected": True,
            "protection_url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/branches/main/protection",
        }
        response_data = create_paginated_response([branch_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/branches"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.repositories.list_branches("testuser", "test-repo")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].name == "main"
        assert result.data[0].protected is True

    @pytest.mark.asyncio
    async def test_get_branch(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test getting a single branch."""
        branch_data = {
            "name": "main",
            "commit_sha": "abc123def456",
            "protected": True,
            "protection_url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/branches/main/protection",
        }
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/branches/main"
        ).mock(return_value=Response(200, json=branch_data))

        result = await client.repositories.get_branch("testuser", "test-repo", "main")

        assert isinstance(result, RepoBranch)
        assert result.name == "main"
        assert result.commit_sha == "abc123def456"


class TestRepositoriesClientTags:
    """Tests for repository tags."""

    @pytest.mark.asyncio
    async def test_list_tags(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test listing tags in a repository."""
        tag_data = {
            "name": "v1.0.0",
            "commit_sha": "abc123def456",
            "tarball_url": "https://sourcecraft.dev/testuser/test-repo/tarball/v1.0.0",
            "zipball_url": "https://sourcecraft.dev/testuser/test-repo/zipball/v1.0.0",
        }
        response_data = create_paginated_response([tag_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/tags"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.repositories.list_tags("testuser", "test-repo")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].name == "v1.0.0"
