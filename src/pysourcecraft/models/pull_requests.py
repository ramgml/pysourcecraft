"""Pydantic models for Pull Requests."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel
from pysourcecraft.models.issues import ReactionCount, UserEmbedded
from pysourcecraft.models.repositories import RepositoryEmbedded


class PRState(str, Enum):
    """Pull request state/status enum."""

    DRAFT = "draft"
    OPEN = "open"
    DISCARDED = "discarded"
    MERGING = "merging"
    MERGED = "merged"


class Side(str, Enum):
    """Diff side enum for anchor position."""

    TARGET = "target"
    SOURCE = "source"


class DiffPos(BaseModel):
    """Diff position for code comments."""

    from_: int = Field(
        ...,
        alias="from",
        description="Start of commented region, line number (1-based)",
    )
    to: int = Field(description="End of commented region, line number (1-based)")
    side: Side | None = Field(None, description="Diff side")
    outdated: bool | None = Field(
        None,
        description="Whether commented region has changed after initial comment publishing",
    )

    model_config = {"populate_by_name": True}


class Hunk(BaseModel):
    """Hunk representing transformation between file versions."""

    from_start: int | None = Field(None, description="Start line in source file")
    from_count: int | None = Field(None, description="Number of lines in source")
    to_start: int | None = Field(None, description="Start line in target file")
    to_count: int | None = Field(None, description="Number of lines in target")
    patch: str | None = Field(None, description="Patch text")


class Anchor(BaseModel):
    """Anchor for code comments - full version with hunk."""

    path: str | None = Field(None, description="Full file path from repository root")
    position: DiffPos | None = Field(None, description="Position in diff")
    hunk: Hunk | None = Field(None, description="Hunk information")


class ShortAnchor(BaseModel):
    """Short anchor for creating code comments."""

    path: str | None = Field(None, description="Full file path from repository root")
    position: DiffPos | None = Field(None, description="Position in diff")


class MergeParameters(BaseModel):
    """Merge parameters for pull request merge."""

    rebase: bool | None = Field(None, description="Whether to rebase")
    squash: bool | None = Field(None, description="Whether to squash")
    delete_branch: bool | None = Field(
        None, description="Whether to delete branch after merge"
    )


class MergeInfo(BaseModel):
    """Merge information for pull request."""

    merger: UserEmbedded | None = Field(
        None, description="User who performed the merge"
    )
    merge_parameters: MergeParameters | None = Field(
        None, description="Parameters used for merge"
    )
    target_commit_hash: str | None = Field(None, description="Target commit hash")
    error: str | None = Field(None, description="Error message if merge failed")
    merge_commit_hash: str | None = Field(
        None, description="Merge commit hash (filled after merge)"
    )


class PRCommentType(str, Enum):
    """Pull request comment type enum."""

    DEFAULT = "default"
    APPSEC = "appsec"


class PRComment(BaseModel):
    """Pull request comment model."""

    id: str = Field(description="Comment ID")
    body: str | None = Field(None, description="Comment body")
    parent_id: str | None = Field(None, description="Parent comment ID for replies")

    # Author information
    author: UserEmbedded = Field(description="Comment author")
    updated_by: UserEmbedded | None = Field(
        None, description="User who last updated the comment"
    )

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    # Status flags
    is_deleted: bool | None = Field(None, description="Whether comment is deleted")
    need_resolution: bool | None = Field(
        None,
        description="Whether this indicates an issue that must be resolved before merge",
    )
    is_resolved: bool | None = Field(
        None, description="Whether the comment/issue is resolved"
    )
    is_published: bool | None = Field(None, description="Whether comment is published")
    is_outdated: bool | None = Field(
        None, description="Whether comment is outdated (code changed)"
    )

    # Reactions
    reactions: dict[str, ReactionCount] | None = Field(
        None, description="Reactions keyed by reaction type"
    )

    # Code anchor for line comments
    anchor: Anchor | None = Field(None, description="Anchor for code comments")

    # Type and iteration
    type: PRCommentType | None = Field(None, description="Comment type")
    iteration: str | None = Field(
        None, description="Iteration specification (defaults to latest)"
    )


class PullRequest(BaseModel):
    """Pull request model matching Sourcecraft API response."""

    # Core identifiers
    id: str = Field(description="Pull request ID")
    slug: str | None = Field(None, description="Pull request slug")

    # Content
    title: str = Field(description="Pull request title")
    description: str | None = Field(None, description="Pull request description")

    # Status
    status: PRState = Field(description="Pull request status")

    # Branches
    source_branch: str = Field(description="Source branch name")
    target_branch: str = Field(description="Target branch name")

    # Author information
    author: UserEmbedded = Field(description="Pull request author")
    updated_by: UserEmbedded | None = Field(
        None, description="User who last updated the PR"
    )

    # Relationships
    repository: RepositoryEmbedded | None = Field(
        None, description="Repository where the PR is located"
    )

    # Merge info
    merge_info: MergeInfo | None = Field(None, description="Merge information")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class CreatePullRequestRequest(BaseModel):
    """Request to create a pull request."""

    title: str = Field(
        ..., max_length=1024, description="Pull request title (up to 1024 characters)"
    )
    description: str | None = Field(
        None, description="Pull request description (up to 10Mb)"
    )
    source_branch: str = Field(description="Source branch name")
    target_branch: str = Field(description="Target branch name")
    fork_repo_id: str | None = Field(
        None, description="Fork repository ID if creating PR from another repository"
    )
    reviewer_ids: list[str] | None = Field(
        None, description="List of user IDs to assign as reviewers"
    )
    publish: bool | None = Field(
        None,
        description="Whether to publish the PR immediately (default: false = draft)",
    )


class UpdatePullRequestRequest(BaseModel):
    """Request to update a pull request."""

    title: str | None = Field(
        None,
        max_length=1024,
        description="Change Pull Request title (up to 1024 characters)",
    )
    description: str | None = Field(
        None, description="Change Pull Request description (up to 10Mb)"
    )


class CreatePullRequestCommentRequest(BaseModel):
    """Request to create a pull request comment."""

    parent_id: str | None = Field(None, description="Parent comment ID for replies")
    body: str = Field(description="Comment body")
    anchor: ShortAnchor | None = Field(
        None, description="Optional anchor for code comments"
    )
    need_resolution: bool | None = Field(
        None, description="Indicates an issue in PR that must be resolved before merge"
    )
    publish: bool | None = Field(
        None, description="Publish immediately (defaults to true)"
    )
    iteration: str | None = Field(
        None,
        description="Optional iteration specification (defaults to latest iteration)",
    )


class PRFilters(BaseModel):
    """Filters for listing pull requests."""

    state: PRState | None = Field(None, description="Filter by state")
    source_branch: str | None = Field(None, description="Filter by source branch")
    target_branch: str | None = Field(None, description="Filter by target branch")
    author_id: str | None = Field(None, description="Filter by author")


# =============================================================================
# Deprecated/Backward Compatibility Models
# These are kept for backward compatibility but marked as deprecated
# =============================================================================


class PRMergeMethod(str, Enum):
    """Pull request merge method enum (deprecated - use MergeParameters instead)."""

    MERGE = "merge"
    SQUASH = "squash"
    REBASE = "rebase"


class PRReviewState(str, Enum):
    """Pull request review state enum (deprecated - Sourcecraft uses PR comments)."""

    PENDING = "pending"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    DISMISSED = "dismissed"
    COMMENTED = "commented"


class PRCheckState(str, Enum):
    """Pull request check state enum (deprecated - Sourcecraft uses CI/CD events)."""

    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"
    SKIPPED = "skipped"


class PRBranch(BaseModel):
    """Pull request branch reference (deprecated - use source_branch/target_branch strings)."""

    ref: str = Field(description="Branch name")
    sha: str = Field(description="Commit SHA")
    repo_id: str = Field(description="Repository ID")


class PRUser(BaseModel):
    """Pull request user reference (deprecated - use UserEmbedded)."""

    id: str = Field(description="User ID")
    username: str = Field(description="Username")
    avatar_url: str | None = Field(None, description="Avatar URL")


class PRReview(BaseModel):
    """Pull request review model (deprecated - Sourcecraft uses PR comments)."""

    id: str = Field(description="Review ID")
    state: PRReviewState = Field(description="Review state")
    body: str | None = Field(None, description="Review body")
    user: PRUser = Field(description="Reviewer")
    submitted_at: datetime | None = Field(None, description="Submission timestamp")
    commit_id: str | None = Field(None, description="Commit SHA")


class PRCheck(BaseModel):
    """Pull request check model (deprecated - Sourcecraft uses CI/CD events)."""

    id: str = Field(description="Check ID")
    name: str = Field(description="Check name")
    state: PRCheckState = Field(description="Check state")
    description: str | None = Field(None, description="Check description")
    target_url: str | None = Field(None, description="Details URL")
    started_at: datetime | None = Field(None, description="Start timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")


class MergePullRequestRequest(BaseModel):
    """Request to merge a pull request (deprecated - use API directly)."""

    commit_title: str | None = Field(None, description="Merge commit title")
    commit_message: str | None = Field(None, description="Merge commit message")
    method: PRMergeMethod = Field(
        default=PRMergeMethod.MERGE, description="Merge method"
    )
    sha: str | None = Field(None, description="Expected head SHA")
