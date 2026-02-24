"""Pydantic models for Pull Requests."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel
from pysourcecraft.models.issues import Label


class PRState(str, Enum):
    """Pull request state enum."""

    OPEN = "open"
    CLOSED = "closed"
    MERGED = "merged"


class PRMergeMethod(str, Enum):
    """Pull request merge method enum."""

    MERGE = "merge"
    SQUASH = "squash"
    REBASE = "rebase"


class PRReviewState(str, Enum):
    """Pull request review state enum."""

    PENDING = "pending"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    DISMISSED = "dismissed"
    COMMENTED = "commented"


class PRCheckState(str, Enum):
    """Pull request check state enum."""

    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"
    SKIPPED = "skipped"


class PRBranch(BaseModel):
    """Pull request branch reference."""

    ref: str = Field(description="Branch name")
    sha: str = Field(description="Commit SHA")
    repo_id: str = Field(description="Repository ID")


class PRUser(BaseModel):
    """Pull request user reference."""

    id: str = Field(description="User ID")
    username: str = Field(description="Username")
    avatar_url: str | None = Field(None, description="Avatar URL")


class PRReview(BaseModel):
    """Pull request review model."""

    id: str = Field(description="Review ID")
    state: PRReviewState = Field(description="Review state")
    body: str | None = Field(None, description="Review body")
    user: PRUser = Field(description="Reviewer")
    submitted_at: datetime | None = Field(None, description="Submission timestamp")
    commit_id: str | None = Field(None, description="Commit SHA")


class PRCheck(BaseModel):
    """Pull request check model."""

    id: str = Field(description="Check ID")
    name: str = Field(description="Check name")
    state: PRCheckState = Field(description="Check state")
    description: str | None = Field(None, description="Check description")
    target_url: str | None = Field(None, description="Details URL")
    started_at: datetime | None = Field(None, description="Start timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")


class PullRequest(BaseModel):
    """Pull request model."""

    id: str = Field(description="PR ID")
    number: int = Field(description="PR number")
    title: str = Field(description="PR title")
    body: str | None = Field(None, description="PR body")
    state: PRState = Field(description="PR state")
    url: str = Field(description="API URL")
    html_url: str = Field(description="HTML URL")
    diff_url: str | None = Field(None, description="Diff URL")
    patch_url: str | None = Field(None, description="Patch URL")

    # Branches
    head: PRBranch = Field(description="Head branch")
    base: PRBranch = Field(description="Base branch")

    # Author
    user: PRUser = Field(description="PR author")

    # Relationships
    assignees: list[PRUser] = Field(default_factory=list, description="Assignees")
    reviewers: list[PRUser] = Field(
        default_factory=list, description="Requested reviewers"
    )
    labels: list[Label] = Field(default_factory=list, description="Labels")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    closed_at: datetime | None = Field(None, description="Closed timestamp")
    merged_at: datetime | None = Field(None, description="Merged timestamp")

    # Merge info
    merged: bool = Field(default=False, description="Whether PR is merged")
    mergeable: bool | None = Field(None, description="Whether PR is mergeable")
    merge_commit_sha: str | None = Field(None, description="Merge commit SHA")
    merged_by: PRUser | None = Field(None, description="User who merged")

    # Counts
    additions: int = Field(default=0, ge=0, description="Lines added")
    deletions: int = Field(default=0, ge=0, description="Lines deleted")
    changed_files: int = Field(default=0, ge=0, description="Files changed")
    comments_count: int = Field(default=0, ge=0, description="Number of comments")
    review_comments_count: int = Field(
        default=0, ge=0, description="Number of review comments"
    )

    # Checks
    checks: list[PRCheck] = Field(default_factory=list, description="Status checks")

    # Draft
    draft: bool = Field(default=False, description="Whether PR is draft")

    # Metadata
    locked: bool = Field(default=False, description="Whether PR is locked")
    maintainer_can_modify: bool = Field(
        default=False, description="Maintainer can modify"
    )


class CreatePullRequestRequest(BaseModel):
    """Request to create a pull request."""

    title: str = Field(min_length=1, max_length=256, description="PR title")
    body: str | None = Field(None, description="PR body")
    head: str = Field(description="Head branch name")
    base: str = Field(description="Base branch name")
    draft: bool = Field(default=False, description="Create as draft")
    maintainer_can_modify: bool = Field(
        default=True, description="Allow maintainer edits"
    )


class UpdatePullRequestRequest(BaseModel):
    """Request to update a pull request."""

    title: str | None = Field(
        None, min_length=1, max_length=256, description="PR title"
    )
    body: str | None = Field(None, description="PR body")
    state: PRState | None = Field(None, description="PR state")
    base: str | None = Field(None, description="Base branch name")
    maintainer_can_modify: bool | None = Field(
        None, description="Allow maintainer edits"
    )


class MergePullRequestRequest(BaseModel):
    """Request to merge a pull request."""

    commit_title: str | None = Field(None, description="Merge commit title")
    commit_message: str | None = Field(None, description="Merge commit message")
    method: PRMergeMethod = Field(
        default=PRMergeMethod.MERGE, description="Merge method"
    )
    sha: str | None = Field(None, description="Expected head SHA")


class PRFilters(BaseModel):
    """Filters for listing pull requests."""

    state: PRState | None = Field(None, description="Filter by state")
    head: str | None = Field(None, description="Filter by head branch")
    base: str | None = Field(None, description="Filter by base branch")
    author_id: str | None = Field(None, description="Filter by author")
    assignee_id: str | None = Field(None, description="Filter by assignee")
