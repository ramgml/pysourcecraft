"""Integration tests for the IssuesClient."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import (
    CreateIssueRequest,
    Issue,
    IssueComment,
    IssueEvent,
    IssueFilters,
    IssueState,
    IssueStateReason,
    PaginatedResponse,
    UpdateIssueRequest,
)

from tests.conftest import create_paginated_response


class TestIssuesClientList:
    """Tests for listing issues."""

    @pytest.mark.asyncio
    async def test_list_issues(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_data: dict[str, Any],
    ) -> None:
        """Test listing issues."""
        response_data = create_paginated_response([mock_issue_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.issues.list("testuser", "test-repo")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.total == 1
        assert result.page == 1

    @pytest.mark.asyncio
    async def test_list_issues_with_filters(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_data: dict[str, Any],
    ) -> None:
        """Test listing issues with filters."""
        response_data = create_paginated_response([mock_issue_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues"
        ).mock(return_value=Response(200, json=response_data))

        filters = IssueFilters(state=IssueState.OPEN, assignee_id="user-123")
        result = await client.issues.list("testuser", "test-repo", filters=filters)

        assert isinstance(result, PaginatedResponse)

    @pytest.mark.asyncio
    async def test_list_issues_pagination(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_data: dict[str, Any],
    ) -> None:
        """Test listing issues with pagination."""
        response_data = create_paginated_response(
            [mock_issue_data], page=2, per_page=10, total=15
        )
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.issues.list("testuser", "test-repo", page=2, per_page=10)

        assert result.page == 2
        assert result.per_page == 10
        assert result.total == 15
        assert result.total_pages == 2
        assert result.has_next is False
        assert result.has_prev is True


class TestIssuesClientGet:
    """Tests for getting a single issue."""

    @pytest.mark.asyncio
    async def test_get_issue(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_data: dict[str, Any],
    ) -> None:
        """Test getting a single issue."""
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues/1"
        ).mock(return_value=Response(200, json=mock_issue_data))

        result = await client.issues.get("testuser", "test-repo", 1)

        assert isinstance(result, Issue)
        assert result.id == "issue-001"
        assert result.number == 1
        assert result.title == "Test Issue"
        assert result.state == IssueState.OPEN


class TestIssuesClientCreate:
    """Tests for creating issues."""

    @pytest.mark.asyncio
    async def test_create_issue(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_data: dict[str, Any],
    ) -> None:
        """Test creating a new issue."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues"
        ).mock(return_value=Response(201, json=mock_issue_data))

        request = CreateIssueRequest(title="Test Issue", body="This is a test issue")
        result = await client.issues.create("testuser", "test-repo", request)

        assert isinstance(result, Issue)
        assert result.title == "Test Issue"

    @pytest.mark.asyncio
    async def test_create_issue_with_assignees_and_labels(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_data: dict[str, Any],
    ) -> None:
        """Test creating an issue with assignees and labels."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues"
        ).mock(return_value=Response(201, json=mock_issue_data))

        request = CreateIssueRequest(
            title="Test Issue",
            body="This is a test issue",
            assignee_ids=["user-123"],
            label_ids=["label-1"],
        )
        await client.issues.create("testuser", "test-repo", request)


class TestIssuesClientUpdate:
    """Tests for updating issues."""

    @pytest.mark.asyncio
    async def test_update_issue(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_data: dict[str, Any],
    ) -> None:
        """Test updating an issue."""
        mock_router.patch(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues/1"
        ).mock(return_value=Response(200, json=mock_issue_data))

        request = UpdateIssueRequest(title="Updated Title")
        result = await client.issues.update("testuser", "test-repo", 1, request)

        assert isinstance(result, Issue)

    @pytest.mark.asyncio
    async def test_close_issue(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_data: dict[str, Any],
    ) -> None:
        """Test closing an issue."""
        mock_router.patch(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues/1"
        ).mock(return_value=Response(200, json=mock_issue_data))

        result = await client.issues.close("testuser", "test-repo", 1)

        assert isinstance(result, Issue)

    @pytest.mark.asyncio
    async def test_reopen_issue(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_data: dict[str, Any],
    ) -> None:
        """Test reopening an issue."""
        mock_router.patch(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues/1"
        ).mock(return_value=Response(200, json=mock_issue_data))

        result = await client.issues.reopen("testuser", "test-repo", 1)

        assert isinstance(result, Issue)


class TestIssuesClientComments:
    """Tests for issue comments."""

    @pytest.mark.asyncio
    async def test_list_comments(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_comment_data: dict[str, Any],
    ) -> None:
        """Test listing issue comments."""
        response_data = create_paginated_response([mock_issue_comment_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues/1/comments"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.issues.list_comments("testuser", "test-repo", 1)

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_create_comment(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_issue_comment_data: dict[str, Any],
    ) -> None:
        """Test creating a comment on an issue."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues/1/comments"
        ).mock(return_value=Response(201, json=mock_issue_comment_data))

        result = await client.issues.create_comment(
            "testuser", "test-repo", 1, "This is a test comment"
        )

        assert isinstance(result, IssueComment)
        assert result.body == "This is a test comment"


class TestIssuesClientEvents:
    """Tests for issue events."""

    @pytest.mark.asyncio
    async def test_list_events(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test listing issue events."""
        event_data = {
            "id": "event-001",
            "event": "labeled",
            "actor": {
                "id": "user-123",
                "username": "testuser",
                "avatar_url": "https://avatars.sourcecraft.dev/u/123",
            },
            "created_at": mock_datetime.isoformat(),
            "label": {
                "id": "label-1",
                "name": "bug",
                "color": "ff0000",
                "description": "Something is broken",
                "created_at": mock_datetime.isoformat(),
                "updated_at": mock_datetime.isoformat(),
            },
            "assignee": None,
            "milestone": None,
        }
        response_data = create_paginated_response([event_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues/1/events"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.issues.list_events("testuser", "test-repo", 1)

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].event == "labeled"
