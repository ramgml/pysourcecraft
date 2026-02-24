"""Tests for Pydantic models validation."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from pysourcecraft.models import (
    # Base
    BaseModel,
    ErrorResponse,
    PaginatedResponse,
    PaginationParams,
    # Issues
    CreateIssueRequest,
    Issue,
    IssueFilters,
    IssueVisibility,
    LabelEmbedded,
    Priority,
    ReactionCount,
    StatusType,
    UpdateIssueRequest,
    UserEmbedded,
    # Pull Requests
    CreatePullRequestRequest,
    MergePullRequestRequest,
    PRCheckState,
    PRMergeMethod,
    PRReviewState,
    PRState,
    CreateRepositoryRequest,
    RepoPermission,
    RepoVisibility,
    Repository,
    UpdateRepositoryRequest,
    # Releases
    CreateReleaseRequest,
    ReleaseState,
    Plan,
    UserType,
    # CI/CD
    PipelineStatus,
    WorkflowConclusion,
    WorkflowEvent,
    WorkflowState,
)


# =============================================================================
# Base Model Tests
# =============================================================================


class TestBaseModel:
    """Tests for the base model."""

    def test_base_model_config(self) -> None:
        """Test base model configuration."""

        class TestModel(BaseModel):
            name: str
            description: str | None = None

        # Test strip whitespace
        model = TestModel(name="  test  ", description="  desc  ")
        assert model.name == "test"
        assert model.description == "desc"

    def test_base_model_extra_ignore(self) -> None:
        """Test that extra fields are ignored."""

        class TestModel(BaseModel):
            name: str

        # Test model_validate ignores extra fields
        model = TestModel.model_validate({"name": "test", "extra_field": "ignored"})
        assert model.name == "test"
        assert not hasattr(model, "extra_field")


class TestPaginationParams:
    """Tests for pagination parameters."""

    def test_default_values(self) -> None:
        """Test default pagination values."""
        params = PaginationParams()
        assert params.page == 1
        assert params.per_page == 30

    def test_custom_values(self) -> None:
        """Test custom pagination values."""
        params = PaginationParams(page=5, per_page=50)
        assert params.page == 5
        assert params.per_page == 50

    def test_page_validation(self) -> None:
        """Test page number validation."""
        with pytest.raises(ValidationError):
            PaginationParams(page=0)

    def test_per_page_validation(self) -> None:
        """Test per_page validation."""
        with pytest.raises(ValidationError):
            PaginationParams(per_page=0)
        with pytest.raises(ValidationError):
            PaginationParams(per_page=101)

    def test_to_query_params(self) -> None:
        """Test conversion to query parameters."""
        params = PaginationParams(page=2, per_page=25)
        query = params.to_query_params()
        assert query == {"page": 2, "per_page": 25}


class TestPaginatedResponse:
    """Tests for paginated response."""

    def test_paginated_response(self) -> None:
        """Test paginated response model."""
        response = PaginatedResponse[dict](
            data=[{"id": "1"}, {"id": "2"}],
            total=10,
            page=1,
            per_page=2,
            total_pages=5,
        )
        assert len(response.data) == 2
        assert response.total == 10
        assert response.has_next is True
        assert response.has_prev is False

    def test_paginated_response_last_page(self) -> None:
        """Test paginated response on last page."""
        response = PaginatedResponse[dict](
            data=[{"id": "9"}, {"id": "10"}],
            total=10,
            page=5,
            per_page=2,
            total_pages=5,
        )
        assert response.has_next is False
        assert response.has_prev is True


class TestErrorModels:
    """Tests for error models."""

    def test_error_response(self) -> None:
        """Test error response model."""
        response = ErrorResponse(
            error_code="ValidationError",
            message="Invalid input",
            request_id="req-123",
            details={"field": "email", "error": "Invalid email"},
        )
        assert response.error_code == "ValidationError"
        assert response.message == "Invalid input"
        assert response.request_id == "req-123"
        assert response.details == {"field": "email", "error": "Invalid email"}

    def test_error_response_minimal(self) -> None:
        """Test error response with minimal fields."""
        response = ErrorResponse(
            error_code="NotFound",
            message="Resource not found",
        )
        assert response.error_code == "NotFound"
        assert response.message == "Resource not found"
        assert response.request_id is None
        assert response.details is None


# =============================================================================
# Issue Model Tests
# =============================================================================


class TestIssueModels:
    """Tests for issue models."""

    def test_priority_enum(self) -> None:
        """Test priority enum."""
        assert Priority.LOW == "low"
        assert Priority.NORMAL == "normal"
        assert Priority.HIGH == "high"
        assert Priority.CRITICAL == "critical"

    def test_issue_visibility_enum(self) -> None:
        """Test issue visibility enum."""
        assert IssueVisibility.PUBLIC == "public"
        assert IssueVisibility.PRIVATE == "private"

    def test_status_type_enum(self) -> None:
        """Test status type enum."""
        assert StatusType.TODO == "todo"
        assert StatusType.IN_PROGRESS == "in_progress"
        assert StatusType.DONE == "done"
        assert StatusType.CANCELED == "canceled"

    def test_user_embedded(self) -> None:
        """Test user embedded model."""
        user = UserEmbedded(id="user-123", slug="testuser")
        assert user.id == "user-123"
        assert user.slug == "testuser"

    def test_label_embedded(self) -> None:
        """Test label embedded model."""
        label = LabelEmbedded(id="label-1", slug="bug", name="Bug", color="ff0000")
        assert label.id == "label-1"
        assert label.slug == "bug"
        assert label.name == "Bug"
        assert label.color == "ff0000"

    def test_reaction_count(self) -> None:
        """Test reaction count model."""
        reaction = ReactionCount(count=5)
        assert reaction.count == 5

    def test_create_issue_request(self) -> None:
        """Test create issue request validation."""
        request = CreateIssueRequest(title="Test Issue", body="Description")
        assert request.title == "Test Issue"
        assert request.body == "Description"

    def test_create_issue_request_title_validation(self) -> None:
        """Test title validation."""
        with pytest.raises(ValidationError):
            CreateIssueRequest(title="")  # Too short
        with pytest.raises(ValidationError):
            CreateIssueRequest(title="x" * 257)  # Too long

    def test_update_issue_request(self) -> None:
        """Test update issue request."""
        request = UpdateIssueRequest(title="Updated Title")
        assert request.title == "Updated Title"
        assert request.body is None

    def test_issue_filters(self) -> None:
        """Test issue filters."""
        filters = IssueFilters(state="open", assignee_id="user-123")
        assert filters.state == "open"
        assert filters.assignee_id == "user-123"


# =============================================================================
# Pull Request Model Tests
# =============================================================================


class TestPullRequestModels:
    """Tests for pull request models."""

    def test_pr_state_enum(self) -> None:
        """Test PR state enum."""
        assert PRState.DRAFT == "draft"
        assert PRState.OPEN == "open"
        assert PRState.DISCARDED == "discarded"
        assert PRState.MERGING == "merging"
        assert PRState.MERGED == "merged"

    def test_pr_merge_method_enum(self) -> None:
        """Test PR merge method enum."""
        assert PRMergeMethod.MERGE == "merge"
        assert PRMergeMethod.SQUASH == "squash"
        assert PRMergeMethod.REBASE == "rebase"

    def test_pr_review_state_enum(self) -> None:
        """Test PR review state enum."""
        assert PRReviewState.PENDING == "pending"
        assert PRReviewState.APPROVED == "approved"
        assert PRReviewState.CHANGES_REQUESTED == "changes_requested"

    def test_pr_check_state_enum(self) -> None:
        """Test PR check state enum."""
        assert PRCheckState.PENDING == "pending"
        assert PRCheckState.SUCCESS == "success"
        assert PRCheckState.FAILURE == "failure"

    def test_create_pull_request_request(self) -> None:
        """Test create PR request."""
        request = CreatePullRequestRequest(
            title="Test PR",
            source_branch="feature",
            target_branch="main",
            publish=True,
        )
        assert request.title == "Test PR"
        assert request.publish is True

    def test_create_pull_request_request_validation(self) -> None:
        """Test PR request validation - title max length."""
        # Title exceeds max_length of 1024
        with pytest.raises(ValidationError):
            CreatePullRequestRequest(
                title="x" * 1025, source_branch="feature", target_branch="main"
            )

    def test_merge_pull_request_request(self) -> None:
        """Test merge PR request."""
        request = MergePullRequestRequest(
            method=PRMergeMethod.SQUASH,
            commit_title="Squashed commit",
        )
        assert request.method == PRMergeMethod.SQUASH


# =============================================================================
# Repository Model Tests
# =============================================================================


class TestRepositoryModels:
    """Tests for repository models."""

    def test_repo_visibility_enum(self) -> None:
        """Test repository visibility enum."""
        assert RepoVisibility.PUBLIC == "public"
        assert RepoVisibility.PRIVATE == "private"
        assert RepoVisibility.INTERNAL == "internal"

    def test_repo_permission_enum(self) -> None:
        """Test repository permission enum."""
        assert RepoPermission.NONE == "none"
        assert RepoPermission.READ == "read"
        assert RepoPermission.WRITE == "write"
        assert RepoPermission.ADMIN == "admin"

    def test_create_repository_request(self) -> None:
        """Test create repository request."""
        request = CreateRepositoryRequest(
            name="test-repo",
            description="A test repo",
            visibility=RepoVisibility.PUBLIC,
        )
        assert request.name == "test-repo"
        assert request.visibility == RepoVisibility.PUBLIC

    def test_create_repository_request_name_validation(self) -> None:
        """Test repository name validation."""
        with pytest.raises(ValidationError):
            CreateRepositoryRequest(name="")
        with pytest.raises(ValidationError):
            CreateRepositoryRequest(name="x" * 101)

    def test_update_repository_request(self) -> None:
        """Test update repository request."""
        request = UpdateRepositoryRequest(description="Updated")
        assert request.description == "Updated"
        assert request.name is None


# =============================================================================
# Release Model Tests
# =============================================================================


class TestReleaseModels:
    """Tests for release models."""

    def test_release_state_enum(self) -> None:
        """Test release state enum."""
        assert ReleaseState.PUBLISHED == "published"
        assert ReleaseState.DRAFT == "draft"
        assert ReleaseState.PRERELEASE == "prerelease"

    def test_create_release_request(self) -> None:
        """Test create release request."""
        request = CreateReleaseRequest(
            tag_name="v1.0.0",
            name="Version 1.0.0",
            body="Release notes",
            draft=True,
        )
        assert request.tag_name == "v1.0.0"
        assert request.draft is True

    def test_create_release_request_validation(self) -> None:
        """Test tag name validation."""
        with pytest.raises(ValidationError):
            CreateReleaseRequest(tag_name="")  # Empty tag name


# =============================================================================
# User Model Tests
# =============================================================================


class TestUserModels:
    """Tests for user models."""

    def test_user_type_enum(self) -> None:
        """Test user type enum."""
        assert UserType.USER == "User"
        assert UserType.ORGANIZATION == "Organization"
        assert UserType.BOT == "Bot"

    def test_plan_model(self) -> None:
        """Test plan model."""
        plan = Plan(
            name="pro",
            space=1000000,
            private_repos=100,
            collaborators=50,
        )
        assert plan.name == "pro"
        assert plan.space == 1000000


# =============================================================================
# CI/CD Model Tests
# =============================================================================


class TestCICDModels:
    """Tests for CI/CD models."""

    def test_workflow_state_enum(self) -> None:
        """Test workflow state enum."""
        assert WorkflowState.QUEUED == "queued"
        assert WorkflowState.IN_PROGRESS == "in_progress"
        assert WorkflowState.COMPLETED == "completed"

    def test_workflow_conclusion_enum(self) -> None:
        """Test workflow conclusion enum."""
        assert WorkflowConclusion.SUCCESS == "success"
        assert WorkflowConclusion.FAILURE == "failure"
        assert WorkflowConclusion.CANCELLED == "cancelled"

    def test_workflow_event_enum(self) -> None:
        """Test workflow event enum."""
        assert WorkflowEvent.PUSH == "push"
        assert WorkflowEvent.PULL_REQUEST == "pull_request"
        assert WorkflowEvent.WORKFLOW_DISPATCH == "workflow_dispatch"

    def test_pipeline_status_enum(self) -> None:
        """Test pipeline status enum."""
        assert PipelineStatus.PENDING == "pending"
        assert PipelineStatus.RUNNING == "running"
        assert PipelineStatus.SUCCESS == "success"
        assert PipelineStatus.FAILED == "failed"


# =============================================================================
# Model Serialization Tests
# =============================================================================


class TestModelSerialization:
    """Tests for model serialization."""

    def test_issue_serialization(self) -> None:
        """Test issue serialization with swagger schema."""
        now = datetime.now(timezone.utc)
        issue_data = {
            "id": "issue-1",
            "slug": "test-issue",
            "title": "Test Issue",
            "description": "Test description",
            "status": {
                "id": "status-1",
                "slug": "open",
                "name": "Open",
                "status_type": "todo",
            },
            "author": {
                "id": "user-1",
                "slug": "testuser",
            },
            "assignee": None,
            "labels": [],
            "linked_prs": [],
            "priority": "normal",
            "visibility": "public",
            "milestone": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        issue = Issue.model_validate(issue_data)
        assert issue.id == "issue-1"
        assert issue.slug == "test-issue"
        assert issue.status.slug == "open"

    def test_repository_serialization(self) -> None:
        """Test repository serialization with Sourcecraft API format."""
        now = datetime.now(timezone.utc)
        repo_data = {
            "id": "repo-1",
            "name": "test-repo",
            "slug": "test-repo",
            "full_name": "owner/test-repo",
            "url": "https://api.example.com/repos/owner/test-repo",
            "html_url": "https://example.com/owner/test-repo",
            "web_url": "https://example.com/owner/test-repo",
            "clone_url": {
                "https": "https://example.com/owner/test-repo.git",
                "ssh": "git@example.com:owner/test-repo.git",
            },
            "owner": {
                "id": "user-1",
                "username": "owner",
                "type": "user",
                "html_url": "https://example.com/owner",
            },
            "visibility": "public",
            "private": False,
            "default_branch": "main",
            "is_empty": False,
            "counters": {
                "forks": "10",
                "issues": "5",
                "pull_requests": "3",
                "tags": "12",
                "branches": "8",
            },
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        repo = Repository.model_validate(repo_data)
        assert repo.name == "test-repo"
        assert repo.visibility == RepoVisibility.PUBLIC
        assert repo.clone_url is not None
        assert repo.clone_url.https == "https://example.com/owner/test-repo.git"
