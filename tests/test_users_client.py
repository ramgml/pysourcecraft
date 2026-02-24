"""Integration tests for the UsersClient and OrganizationsClient."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import (
    OrgMembership,
    Organization,
    PaginatedResponse,
    User,
    UserType,
)

from tests.conftest import create_paginated_response


class TestUsersClientGet:
    """Tests for getting users."""

    @pytest.mark.asyncio
    async def test_get_current_user(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_user_data: dict[str, Any],
    ) -> None:
        """Test getting the authenticated user."""
        mock_router.get("https://api.sourcecraft.dev/v1/user").mock(
            return_value=Response(200, json=mock_user_data)
        )

        result = await client.users.get_current()

        assert isinstance(result, User)
        assert result.id == "user-123"
        assert result.username == "testuser"
        assert result.type == UserType.USER

    @pytest.mark.asyncio
    async def test_get_user_by_username(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_user_data: dict[str, Any],
    ) -> None:
        """Test getting a user by username."""
        mock_router.get("https://api.sourcecraft.dev/v1/users/testuser").mock(
            return_value=Response(200, json=mock_user_data)
        )

        result = await client.users.get("testuser")

        assert isinstance(result, User)
        assert result.username == "testuser"


class TestUsersClientUpdate:
    """Tests for updating users."""

    @pytest.mark.asyncio
    async def test_update_user(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_user_data: dict[str, Any],
    ) -> None:
        """Test updating the authenticated user."""
        updated_data = {**mock_user_data, "bio": "Updated bio"}
        mock_router.patch("https://api.sourcecraft.dev/v1/user").mock(
            return_value=Response(200, json=updated_data)
        )

        result = await client.users.update(bio="Updated bio")

        assert isinstance(result, User)
        assert result.bio == "Updated bio"


class TestUsersClientRepos:
    """Tests for user repositories."""

    @pytest.mark.asyncio
    async def test_list_user_repos(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test listing repositories for a user."""
        response_data = create_paginated_response([mock_repository_data], total=1)
        mock_router.get("https://api.sourcecraft.dev/v1/users/testuser/repos").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.users.list_repos("testuser")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_list_current_user_repos(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test listing repositories for the authenticated user."""
        response_data = create_paginated_response([mock_repository_data], total=1)
        mock_router.get("https://api.sourcecraft.dev/v1/repos").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.users.list_repos()

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1


class TestUsersClientOrgs:
    """Tests for user organizations."""

    @pytest.mark.asyncio
    async def test_list_user_orgs(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_organization_data: dict[str, Any],
    ) -> None:
        """Test listing organizations for a user."""
        response_data = create_paginated_response([mock_organization_data], total=1)
        mock_router.get("https://api.sourcecraft.dev/v1/users/testuser/orgs").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.users.list_orgs("testuser")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].login == "testorg"

    @pytest.mark.asyncio
    async def test_list_current_user_orgs(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_organization_data: dict[str, Any],
    ) -> None:
        """Test listing organizations for the authenticated user."""
        response_data = create_paginated_response([mock_organization_data], total=1)
        mock_router.get("https://api.sourcecraft.dev/v1/user/orgs").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.users.list_orgs()

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1


class TestOrganizationsClientList:
    """Tests for listing organizations."""

    @pytest.mark.asyncio
    async def test_list_organizations(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_organization_data: dict[str, Any],
    ) -> None:
        """Test listing all organizations."""
        response_data = create_paginated_response([mock_organization_data], total=1)
        mock_router.get("https://api.sourcecraft.dev/v1/organizations").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.organizations.list()

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].id == "org-456"


class TestOrganizationsClientGet:
    """Tests for getting organizations."""

    @pytest.mark.asyncio
    async def test_get_organization(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_organization_data: dict[str, Any],
    ) -> None:
        """Test getting an organization."""
        mock_router.get("https://api.sourcecraft.dev/v1/orgs/testorg").mock(
            return_value=Response(200, json=mock_organization_data)
        )

        result = await client.organizations.get("testorg")

        assert isinstance(result, Organization)
        assert result.id == "org-456"
        assert result.login == "testorg"
        assert result.type == UserType.ORGANIZATION


class TestOrganizationsClientUpdate:
    """Tests for updating organizations."""

    @pytest.mark.asyncio
    async def test_update_organization(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_organization_data: dict[str, Any],
    ) -> None:
        """Test updating an organization."""
        updated_data = {**mock_organization_data, "description": "Updated description"}
        mock_router.patch("https://api.sourcecraft.dev/v1/orgs/testorg").mock(
            return_value=Response(200, json=updated_data)
        )

        result = await client.organizations.update(
            "testorg", description="Updated description"
        )

        assert isinstance(result, Organization)
        assert result.description == "Updated description"


class TestOrganizationsClientRepos:
    """Tests for organization repositories."""

    @pytest.mark.asyncio
    async def test_list_org_repos(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_repository_data: dict[str, Any],
    ) -> None:
        """Test listing repositories for an organization."""
        response_data = create_paginated_response([mock_repository_data], total=1)
        mock_router.get("https://api.sourcecraft.dev/v1/orgs/testorg/repos").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.organizations.list_repos("testorg")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1


class TestOrganizationsClientMembers:
    """Tests for organization members."""

    @pytest.mark.asyncio
    async def test_list_members(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_user_data: dict[str, Any],
    ) -> None:
        """Test listing members of an organization."""
        response_data = create_paginated_response([mock_user_data], total=1)
        mock_router.get("https://api.sourcecraft.dev/v1/orgs/testorg/members").mock(
            return_value=Response(200, json=response_data)
        )

        result = await client.organizations.list_members("testorg")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_get_membership(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test getting membership of a user in an organization."""
        membership_data = {
            "id": "membership-001",
            "state": "active",
            "role": "admin",
            "organization_id": "org-456",
            "organization_login": "testorg",
            "user_id": "user-123",
            "user_username": "testuser",
            "created_at": mock_datetime.isoformat(),
            "updated_at": mock_datetime.isoformat(),
        }
        mock_router.get(
            "https://api.sourcecraft.dev/v1/orgs/testorg/memberships/testuser"
        ).mock(return_value=Response(200, json=membership_data))

        result = await client.organizations.get_membership("testorg", "testuser")

        assert isinstance(result, OrgMembership)
        assert result.state == "active"
        assert result.role == "admin"
