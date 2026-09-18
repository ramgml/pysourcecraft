"""Pytest configuration and fixtures for pysourcecraft tests."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from datetime import datetime, timezone
from typing import Any

import pytest
import pytest_asyncio
import respx

from pysourcecraft.client import SourceCraftClient


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
    """Return mock user data matching UserProfile schema."""
    return {
        "id": "user-123",
        "display_name": "Test User",
        "username": "testuser",
        "bio": "A test user",
        "location": {
            "country": "USA",
            "city": "San Francisco",
        },
        "timezone": {
            "iana_timezone": "America/Los_Angeles",
        },
        "workplace": {
            "company": "Test Corp",
            "position": "Developer",
        },
        "links": [
            {"link": "https://blog.example.com", "type": "blog"},
        ],
        "status": {
            "message": "Working on code",
            "emoji": "💻",
        },
        "avatar": {
            "url": "https://avatars.sourcecraft.dev/u/123",
        },
        "background_image": None,
        "visibility": "public",
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
    """Return mock repository data matching Sourcecraft API response."""
    return {
        "id": "repo-789",
        "name": "test-repo",
        "slug": "test-repo",
        "full_name": "testuser/test-repo",
        "description": "A test repository",
        "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo",
        "html_url": "https://sourcecraft.dev/testuser/test-repo",
        "web_url": "https://sourcecraft.dev/testuser/test-repo",
        "clone_url": {
            "https": "https://sourcecraft.dev/testuser/test-repo.git",
            "ssh": "git@sourcecraft.dev:testuser/test-repo.git",
        },
        "ssh_url": "git@sourcecraft.dev:testuser/test-repo.git",
        "owner": {
            "id": "user-123",
            "username": "testuser",
            "type": "user",
            "avatar_url": "https://avatars.sourcecraft.dev/u/123",
            "html_url": "https://sourcecraft.dev/testuser",
        },
        "organization": {
            "id": "org-456",
            "slug": "testorg",
        },
        "visibility": "public",
        "private": False,
        "is_empty": False,
        "template_type": "not_a_template",
        "default_branch": "main",
        "homepage": "https://test-repo.example.com",
        "wiki_url": "https://sourcecraft.dev/testuser/test-repo/wiki",
        "issues_url": "https://sourcecraft.dev/testuser/test-repo/issues",
        "pulls_url": "https://sourcecraft.dev/testuser/test-repo/pulls",
        "logo": {
            "url": "https://sourcecraft.dev/testuser/test-repo/logo.png",
            "width": 128,
            "height": 128,
        },
        "links": [
            {"link": "https://test-repo.example.com", "type": "homepage"},
            {"link": "https://twitter.com/testrepo", "type": "social_network"},
        ],
        "counters": {
            "forks": "10",
            "issues": "5",
            "pull_requests": "3",
            "tags": "12",
            "branches": "8",
        },
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
        "language": {
            "name": "Python",
            "color": "#3572A5",
        },
        "languages": [
            {"name": "Python", "bytes_count": 50000, "percentage": 80.0},
            {"name": "JavaScript", "bytes_count": 12500, "percentage": 20.0},
        ],
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "pushed_at": mock_datetime.isoformat(),
        "last_updated": mock_datetime.isoformat(),
        "fork": False,
        "parent": None,
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
    """Return mock issue data matching swagger schema."""
    return {
        "id": "issue-001",
        "slug": "test-issue",
        "title": "Test Issue",
        "description": "This is a test issue",
        "status": {
            "id": "status-001",
            "slug": "open",
            "name": "Open",
            "status_type": "todo",
        },
        "author": {
            "id": "user-123",
            "slug": "testuser",
        },
        "updated_by": None,
        "assignee": None,
        "labels": [
            {
                "id": "label-1",
                "slug": "bug",
                "name": "bug",
                "color": "ff0000",
            }
        ],
        "linked_prs": [],
        "priority": "normal",
        "visibility": "public",
        "milestone": None,
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "deadline": None,
        "started_at": None,
        "completed_at": None,
    }


@pytest.fixture
def mock_issue_comment_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock issue comment data matching swagger schema."""
    return {
        "id": "comment-001",
        "body": "This is a test comment",
        "parent": None,
        "author": {
            "id": "user-123",
            "slug": "testuser",
        },
        "updated_by": None,
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "reactions": {
            "+1": {"count": 2},
            "-1": {"count": 0},
            "laugh": {"count": 1},
        },
        "attachments": [],
    }


@pytest.fixture
def mock_pull_request_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock pull request data matching Sourcecraft API schema."""
    return {
        "id": "pr-001",
        "slug": "test-pr",
        "title": "Test Pull Request",
        "description": "This is a test PR",
        "status": "open",
        "source_branch": "feature-branch",
        "target_branch": "main",
        "author": {
            "id": "user-123",
            "slug": "testuser",
        },
        "updated_by": None,
        "repository": {
            "id": "repo-789",
            "slug": "test-repo",
        },
        "merge_info": None,
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
    }


@pytest.fixture
def mock_release_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock release data matching swagger schema."""
    return {
        "id": "release-001",
        "repo_id": "repo-789",
        "author": {
            "id": "user-123",
            "slug": "testuser",
        },
        "tag": "v1.0.0",
        "hash": "abc123def456",
        "title": "Version 1.0.0",
        "release_notes": "Initial release",
        "status": "published",
        "assets": [
            {
                "id": "asset-001",
                "name": "app-v1.0.0.zip",
                "link": "https://sourcecraft.dev/testuser/test-repo/releases/download/v1.0.0/app-v1.0.0.zip",
                "attachment": {
                    "id": "attachment-001",
                    "name": "app-v1.0.0.zip",
                    "mime_type": "application/zip",
                    "file_type": "archive",
                    "size": "1024000",
                },
            }
        ],
        "is_latest": True,
        "is_pre_release": False,
        "created_at": mock_datetime.isoformat(),
        "updated_at": mock_datetime.isoformat(),
        "released_at": mock_datetime.isoformat(),
    }


@pytest.fixture
def mock_run_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock CI/CD run data matching swagger Run schema."""
    return {
        "id": "",
        "slug": "12",
        "dates": {
            "created_at": mock_datetime.isoformat(),
            "started_at": mock_datetime.isoformat(),
            "finished_at": mock_datetime.isoformat(),
            "updated_at": mock_datetime.isoformat(),
        },
        "status": "success",
        "workflows": [
            {
                "id": "",
                "slug": "ci",
                "description": "Main pipeline",
                "dates": {"created_at": mock_datetime.isoformat()},
                "status": "success",
                "tasks": [
                    {
                        "id": "",
                        "slug": "build",
                        "status": "success",
                        "cubes": [
                            {
                                "id": "",
                                "slug": "package",
                                "status": "success",
                                "artifacts": [
                                    {
                                        "id": "",
                                        "local_path": "dist/app.whl",
                                        "dates": {
                                            "registered_at": mock_datetime.isoformat()
                                        },
                                        "status": "success",
                                        "download_url": "https://sourcecraft.dev/dl/app.whl",
                                    }
                                ],
                            }
                        ],
                        "progress": {"percent": 1.0},
                    }
                ],
                "progress": {"percent": 1.0},
            }
        ],
        "event_type": "push",
        "error_messages": [],
        "pull": None,
        "user": {"id": "user-123", "slug": "testuser"},
    }


@pytest.fixture
def mock_logs_data() -> dict[str, Any]:
    """Return mock cube logs response matching swagger GetCubeLogsResponse."""
    return {"logs": "[2024-01-15] build started\n", "page_complete": True, "done": True}


@pytest.fixture
def mock_cube_artifacts_data(mock_datetime: datetime) -> dict[str, Any]:
    """Return mock cube artifacts response matching swagger GetCubeArtifactsResponse."""
    return {
        "artifacts": [
            {
                "id": "",
                "local_path": "dist/app.whl",
                "dates": {
                    "registered_at": mock_datetime.isoformat(),
                    "obtained_at": mock_datetime.isoformat(),
                    "updated_at": mock_datetime.isoformat(),
                },
                "status": "success",
                "download_url": "https://sourcecraft.dev/dl/app.whl",
            }
        ]
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


def create_runs_response(
    runs: list[dict[str, Any]],
    next_page_token: str | None = None,
) -> dict[str, Any]:
    """Create a ListRunsResponse structure (token-paginated)."""
    response: dict[str, Any] = {"runs": runs}
    if next_page_token:
        response["next_page_token"] = next_page_token
    return response


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
