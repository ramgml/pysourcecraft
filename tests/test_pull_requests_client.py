"""Integration tests for the PullRequestsClient."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import (
    CreatePullRequestRequest,
    MergePullRequestRequest,
    PRFilters,
    PRMergeMethod,
    PRReview,
    PRReviewState,
    PRCheckState,
    PaginatedResponse,
    PullRequest,
    PRState,
    UpdatePullRequestRequest,
)

from tests.conftest import create_paginated_response


class TestPullRequestsClientList:
    """Tests for listing pull requests."""

    @pytest.mark.asyncio
    async def test_list_pull_requests(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pull_request_data: dict[str, Any],
    ) -> None:
        """Test listing pull requests."""
        response_data = create_paginated_response([mock_pull_request_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.pull_requests.list("testuser", "test-repo")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.total == 1

    @pytest.mark.asyncio
    async def test_list_pull_requests_with_filters(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pull_request_data: dict[str, Any],
    ) -> None:
        """Test listing pull requests with filters."""
        response_data = create_paginated_response([mock_pull_request_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls"
        ).mock(return_value=Response(200, json=response_data))

        filters = PRFilters(state=PRState.OPEN, target_branch="main")
        result = await client.pull_requests.list(
            "testuser", "test-repo", filters=filters
        )

        assert isinstance(result, PaginatedResponse)


class TestPullRequestsClientGet:
    """Tests for getting a single pull request."""

    @pytest.mark.asyncio
    async def test_get_pull_request(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pull_request_data: dict[str, Any],
    ) -> None:
        """Test getting a single pull request."""
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls/1"
        ).mock(return_value=Response(200, json=mock_pull_request_data))

        result = await client.pull_requests.get("testuser", "test-repo", 1)

        assert isinstance(result, PullRequest)
        assert result.id == "pr-001"
        assert result.slug == "test-pr"
        assert result.title == "Test Pull Request"
        assert result.status == PRState.OPEN


class TestPullRequestsClientCreate:
    """Tests for creating pull requests."""

    @pytest.mark.asyncio
    async def test_create_pull_request(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pull_request_data: dict[str, Any],
    ) -> None:
        """Test creating a new pull request."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls"
        ).mock(return_value=Response(201, json=mock_pull_request_data))

        request = CreatePullRequestRequest(
            title="Test Pull Request",
            description="This is a test PR",
            source_branch="feature-branch",
            target_branch="main",
        )
        result = await client.pull_requests.create("testuser", "test-repo", request)

        assert isinstance(result, PullRequest)
        assert result.title == "Test Pull Request"

    @pytest.mark.asyncio
    async def test_create_draft_pull_request(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pull_request_data: dict[str, Any],
    ) -> None:
        """Test creating a draft pull request."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls"
        ).mock(return_value=Response(201, json=mock_pull_request_data))

        request = CreatePullRequestRequest(
            title="WIP: Test PR",
            source_branch="feature-branch",
            target_branch="main",
            publish=False,
        )
        result = await client.pull_requests.create("testuser", "test-repo", request)

        assert isinstance(result, PullRequest)


class TestPullRequestsClientUpdate:
    """Tests for updating pull requests."""

    @pytest.mark.asyncio
    async def test_update_pull_request(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pull_request_data: dict[str, Any],
    ) -> None:
        """Test updating a pull request."""
        mock_router.patch(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls/1"
        ).mock(return_value=Response(200, json=mock_pull_request_data))

        request = UpdatePullRequestRequest(title="Updated Title")
        result = await client.pull_requests.update("testuser", "test-repo", 1, request)

        assert isinstance(result, PullRequest)


class TestPullRequestsClientMerge:
    """Tests for merging pull requests."""

    @pytest.mark.asyncio
    async def test_merge_pull_request(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test merging a pull request."""
        mock_router.put(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls/1/merge"
        ).mock(
            return_value=Response(
                200,
                json={"sha": "merge-commit-sha", "merged": True, "message": "Merged"},
            )
        )

        result = await client.pull_requests.merge("testuser", "test-repo", 1)

        assert result["merged"] is True
        assert result["sha"] == "merge-commit-sha"

    @pytest.mark.asyncio
    async def test_merge_with_method(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test merging with specific method."""
        mock_router.put(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls/1/merge"
        ).mock(
            return_value=Response(
                200,
                json={"sha": "merge-commit-sha", "merged": True, "message": "Merged"},
            )
        )

        request = MergePullRequestRequest(
            method=PRMergeMethod.SQUASH,
            commit_title="Squashed commit",
        )
        await client.pull_requests.merge("testuser", "test-repo", 1, request)


class TestPullRequestsClientReviews:
    """Tests for pull request reviews."""

    @pytest.mark.asyncio
    async def test_list_reviews(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test listing reviews on a pull request."""
        review_data = {
            "id": "review-001",
            "state": "approved",
            "body": "LGTM!",
            "user": {
                "id": "user-456",
                "username": "reviewer",
                "avatar_url": "https://avatars.sourcecraft.dev/u/456",
            },
            "submitted_at": mock_datetime.isoformat(),
            "commit_id": "abc123",
        }
        response_data = create_paginated_response([review_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls/1/reviews"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.pull_requests.list_reviews("testuser", "test-repo", 1)

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].state == PRReviewState.APPROVED

    @pytest.mark.asyncio
    async def test_create_review(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test creating a review on a pull request."""
        review_data = {
            "id": "review-001",
            "state": "commented",
            "body": "Please fix this",
            "user": {
                "id": "user-123",
                "username": "testuser",
                "avatar_url": "https://avatars.sourcecraft.dev/u/123",
            },
            "submitted_at": mock_datetime.isoformat(),
            "commit_id": None,
        }
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls/1/reviews"
        ).mock(return_value=Response(201, json=review_data))

        result = await client.pull_requests.create_review(
            "testuser", "test-repo", 1, body="Please fix this", event="COMMENT"
        )

        assert isinstance(result, PRReview)
        assert result.body == "Please fix this"


class TestPullRequestsClientChecks:
    """Tests for pull request checks."""

    @pytest.mark.asyncio
    async def test_list_checks(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test listing status checks on a pull request."""
        check_data = {
            "id": "check-001",
            "name": "CI / Test",
            "state": "success",
            "description": "All tests passed",
            "target_url": "https://ci.sourcecraft.dev/run/1",
            "started_at": mock_datetime.isoformat(),
            "completed_at": mock_datetime.isoformat(),
        }
        response_data = create_paginated_response([check_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls/1/checks"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.pull_requests.list_checks("testuser", "test-repo", 1)

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].state == PRCheckState.SUCCESS
