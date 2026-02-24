"""Pytest configuration and fixtures for pysourcecraft tests."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from datetime import datetime, timezone
from typing import Any

import pytest
import pytest_asyncio
import respx
from httpx import Response

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import (
    Issue,
    IssueState,
    IssueStateReason,
    PullRequest,
    PRState,
    Repository,
    RepoVisibility,
    Release,
    ReleaseState,
    User,
    UserType,
    WorkflowRun,
    WorkflowState,
    WorkflowEvent,
    Pipeline,
    PipelineStatus,
)


# =============================================================================
# Client Fixtures
# =============================================================================


@pytest_asyncio.fixture
async def client() -> AsyncIterator[SourceCraftClient]:
    """Create a SourceCraftClient for testing."""
    client = SourceCraftClient(
        api_token="test-token",
        base_url="https://api.sourcecraft.dev/v1",
    )
    yield client
    await client.close()


@pytest_asyncio.fixture
async def client_no_auth() -> AsyncIterator[SourceCraftClient]:
    """Create a SourceCraftClient without authentication."""
    client = SourceCraftClient(
        api_token=None,
        base_url="https://api.sourcecraft.dev/v1",
    )
    yield client
    await client.close()


@pytest.fixture
def mock_router() -> Iterator[respx.MockRouter]:
    """Create a respx mock router."""
    with respx.mock(assert_all_mocked=False, assert_all_called=False) as respx_mock:
        yield respx_mock


# =============================================================================
# Mock Data Fixtures
# =============================================================================


@pytest.fixture
def mock_datetime() -> datetime:
    """Return a fixed datetime for testing."""
    return datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)


@pytest.fixture
def mock_user_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock user data."""
    return {
        "id": "user-123",
        "username": "testuser",
        "type": "User",
        "name": "Test User",
        "email": "test@example.com",
        "bio": "A test user",
        "blog": "https://blog.example.com",
        "company": "Test Corp",
        "location": "San Francisco",
        "hireable": True,
        "url": "https://api.sourcecraft.dev/v1/users/testuser",
        "html_url": "https://sourcecraft.dev/testuser",
        "avatar_url": "https://avatars.sourcecraft.dev/u/123",
        "gravatar_id": "",
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "twitter_username": "testuser",
        "followers_count": 100,
        "following_count": 50,
        "public_repos_count": 25,
        "public_gists_count": 10,
        "private_gists_count": 5,
        "two_factor_authentication": True,
        "site_admin": False,
    }


@pytest.fixture
def mock_organization_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock organization data."""
    return {
        "id": "org-456",
        "login": "testorg",
        "type": "Organization",
        "name": "Test Organization",
        "description": "A test organization",
        "email": "org@example.com",
        "blog": "https://org.example.com",
        "location": "New York",
        "company": None,
        "url": "https://api.sourcecraft.dev/v1/orgs/testorg",
        "html_url": "https://sourcecraft.dev/testorg",
        "avatar_url": "https://avatars.sourcecraft.dev/o/456",
        "gravatar_id": "",
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "public_repos_count": 50,
        "followers_count": 200,
        "following_count": 0,
        "members_count": 25,
        "plan": {
            "name": "pro",
            "space": 1000000,
            "private_repos": 100,
            "collaborators": 50,
        },
        "default_repository_permission": "read",
        "members_can_create_repos": True,
        "members_can_create_public_repos": True,
        "members_can_create_private_repos": True,
        "two_factor_requirement_enabled": True,
    }


@pytest.fixture
def mock_repository_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock repository data."""
    return {
        "id": "repo-789",
        "name": "test-repo",
        "full_name": "testuser/test-repo",
        "description": "A test repository",
        "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo",
        "html_url": "https://sourcecraft.dev/testuser/test-repo",
        "clone_url": "https://sourcecraft.dev/testuser/test-repo.git",
        "ssh_url": "git@sourcecraft.dev:testuser/test-repo.git",
        "owner": {
            "id": "user-123",
            "username": "testuser",
            "type": "user",
            "avatar_url": "https://avatars.sourcecraft.dev/u/123",
            "html_url": "https://sourcecraft.dev/testuser",
        },
        "visibility": "public",
        "private": False,
        "default_branch": "main",
        "homepage": "https://test-repo.example.com",
        "wiki_url": "https://sourcecraft.dev/testuser/test-repo/wiki",
        "issues_url": "https://sourcecraft.dev/testuser/test-repo/issues",
        "pulls_url": "https://sourcecraft.dev/testuser/test-repo/pulls",
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "has_discussions": False,
        "has_pages": False,
        "allow_forking": True,
        "allow_squash_merge": True,
        "allow_merge_commit": True,
        "allow_rebase_merge": True,
        "delete_branch_on_merge": False,
        "squash_merge_commit_title": "PR_TITLE",
        "squash_merge_commit_message": "PR_BODY",
        "merge_commit_title": "PR_TITLE",
        "merge_commit_message": "PR_BODY",
        "topics": ["python", "testing"],
        "license": {
            "key": "mit",
            "name": "MIT License",
            "spdx_id": "MIT",
            "url": "https://api.sourcecraft.dev/v1/licenses/mit",
        },
        "language": "Python",
        "languages": [
            {"name": "Python", "bytes_count": 50000, "percentage": 80.0},
            {"name": "JavaScript", "bytes_count": 12500, "percentage": 20.0},
        ],
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "pushed_at": mock_datetime.isoformat(),
        "fork": False,
        "parent_id": None,
        "forks_count": 10,
        "stargazers_count": 50,
        "watchers_count": 50,
        "open_issues_count": 5,
        "open_pulls_count": 3,
        "size_kb": 1024,
        "archived": False,
        "disabled": False,
        "is_template": False,
        "permissions": {"admin": True, "push": True, "pull": True},
    }


@pytest.fixture
def mock_issue_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock issue data."""
    return {
        "id": "issue-001",
        "number": 1,
        "title": "Test Issue",
        "body": "This is a test issue",
        "state": "open",
        "state_reason": None,
        "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues/1",
        "html_url": "https://sourcecraft.dev/testuser/test-repo/issues/1",
        "creator": {
            "id": "user-123",
            "username": "testuser",
            "avatar_url": "https://avatars.sourcecraft.dev/u/123",
        },
        "assignees": [],
        "labels": [
            {
                "id": "label-1",
                "name": "bug",
                "color": "ff0000",
                "description": "Something is broken",
                "created_at": mock_datetime.isoformat(),
                "updated_at": mock_datetime.isoformat(),
            }
        ],
        "milestone": None,
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "closed_at": None,
        "comments_count": 0,
        "locked": False,
    }


@pytest.fixture
def mock_issue_comment_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock issue comment data."""
    return {
        "id": "comment-001",
        "body": "This is a test comment",
        "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/issues/comments/1",
        "html_url": "https://sourcecraft.dev/testuser/test-repo/issues/1#issuecomment-1",
        "user": {
            "id": "user-123",
            "username": "testuser",
            "avatar_url": "https://avatars.sourcecraft.dev/u/123",
        },
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "reactions": {"+1": 2, "-1": 0, "laugh": 1},
    }


@pytest.fixture
def mock_pull_request_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock pull request data."""
    return {
        "id": "pr-001",
        "number": 1,
        "title": "Test Pull Request",
        "body": "This is a test PR",
        "state": "open",
        "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pulls/1",
        "html_url": "https://sourcecraft.dev/testuser/test-repo/pulls/1",
        "diff_url": "https://sourcecraft.dev/testuser/test-repo/pulls/1.diff",
        "patch_url": "https://sourcecraft.dev/testuser/test-repo/pulls/1.patch",
        "head": {
            "ref": "feature-branch",
            "sha": "abc123def456",
            "repo_id": "repo-789",
        },
        "base": {
            "ref": "main",
            "sha": "def789abc012",
            "repo_id": "repo-789",
        },
        "user": {
            "id": "user-123",
            "username": "testuser",
            "avatar_url": "https://avatars.sourcecraft.dev/u/123",
        },
        "assignees": [],
        "reviewers": [],
        "labels": [],
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "closed_at": None,
        "merged_at": None,
        "merged": False,
        "mergeable": True,
        "merge_commit_sha": None,
        "merged_by": None,
        "additions": 100,
        "deletions": 50,
        "changed_files": 5,
        "comments_count": 3,
        "review_comments_count": 2,
        "checks": [],
        "draft": False,
        "locked": False,
        "maintainer_can_modify": True,
    }


@pytest.fixture
def mock_release_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock release data."""
    return {
        "id": "release-001",
        "tag_name": "v1.0.0",
        "name": "Version 1.0.0",
        "body": "Initial release",
        "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/releases/1",
        "html_url": "https://sourcecraft.dev/testuser/test-repo/releases/tag/v1.0.0",
        "tarball_url": "https://sourcecraft.dev/testuser/test-repo/tarball/v1.0.0",
        "zipball_url": "https://sourcecraft.dev/testuser/test-repo/zipball/v1.0.0",
        "author": {
            "id": "user-123",
            "username": "testuser",
            "avatar_url": "https://avatars.sourcecraft.dev/u/123",
        },
        "target_commitish": "main",
        "draft": False,
        "prerelease": False,
        "created_at": mock_datetime.isoformat(),
        "published_at": mock_datetime.isoformat(),
        "assets": [
            {
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
        ],
        "discussion_url": None,
        "reactions": {"+1": 10, "-1": 0},
    }


@pytest.fixture
def mock_workflow_run_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock workflow run data."""
    return {
        "id": "run-001",
        "name": "CI",
        "run_number": 42,
        "run_attempt": 1,
        "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs/1",
        "html_url": "https://sourcecraft.dev/testuser/test-repo/actions/runs/1",
        "state": "completed",
        "conclusion": "success",
        "event": "push",
        "head_branch": "main",
        "head_sha": "abc123def456",
        "head_commit_message": "Fix bug in parser",
        "actor_id": "user-123",
        "actor_username": "testuser",
        "triggering_actor_id": None,
        "triggering_actor_username": None,
        "repository_id": "repo-789",
        "repository_name": "test-repo",
        "pull_request_number": None,
        "pull_request_url": None,
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "run_started_at": mock_datetime.isoformat(),
        "completed_at": mock_datetime.isoformat(),
        "duration_seconds": 120,
        "jobs_url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs/1/jobs",
        "logs_url": "https://sourcecraft.dev/testuser/test-repo/actions/runs/1/logs",
        "check_suite_url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/check-suites/1",
        "artifacts_url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs/1/artifacts",
        "cancel_url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs/1/cancel",
        "rerun_url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs/1/rerun",
        "jobs_count": 3,
        "jobs_completed": 3,
        "jobs_failed": 0,
        "path": ".github/workflows/ci.yml",
        "display_title": "Fix bug in parser",
    }


@pytest.fixture
def mock_pipeline_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock pipeline data."""
    return {
        "id": "pipeline-001",
        "name": "Test Pipeline",
        "status": "success",
        "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pipelines/1",
        "web_url": "https://sourcecraft.dev/testuser/test-repo/pipelines/1",
        "repository_id": "repo-789",
        "ref": "main",
        "sha": "abc123def456",
        "source": "push",
        "trigger_id": "user-123",
        "trigger_username": "testuser",
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "started_at": mock_datetime.isoformat(),
        "finished_at": mock_datetime.isoformat(),
        "duration_seconds": 300,
        "stages": [],
        "coverage": 85.5,
    }


# =============================================================================
# Helper Functions
# =============================================================================


def create_paginated_response(
    data: list[dict[str, Any]],
    page: int = 1,
    per_page: int = 30,
    total: int | None = None,
) -> dict[str, Any]:
    """Create a paginated response structure."""
    total = total if total is not None else len(data)
    total_pages = (total + per_page - 1) // per_page
    return {
        "data": data,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
    }


def create_error_response(
    error: str,
    message: str,
    status_code: int,
    details: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create an error response structure."""
    return {
        "error": error,
        "message": message,
        "details": details or [],
        "status_code": status_code,
    }
