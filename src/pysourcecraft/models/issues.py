"""Pydantic models for Issues."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel


class Priority(str, Enum):
    """Issue priority enum."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class IssueVisibility(str, Enum):
    """Issue visibility enum."""

    PUBLIC = "public"
    PRIVATE = "private"


class StatusType(str, Enum):
    """Issue status type enum."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELED = "canceled"


class UserEmbedded(BaseModel):
    """Embedded user reference."""

    id: str = Field(description="User ID")
    slug: str = Field(description="User slug")


class IssueStatus(BaseModel):
    """Issue status model."""

    id: str = Field(description="Status ID")
    slug: str = Field(description="Status slug")
    name: str = Field(description="Status name")
    status_type: StatusType = Field(description="Status type")


class LabelEmbedded(BaseModel):
    """Embedded label reference."""

    id: str = Field(description="Label ID")
    slug: str = Field(description="Label slug")
    name: str = Field(description="Label name")
    color: str = Field(description="Label color (hex)")


class Label(BaseModel):
    """Label model (v1.Label)."""

    id: str = Field(description="Label ID")
    name: str = Field(description="Label name")
    slug: str = Field(description="Label slug")
    color: str = Field(description="Label color (hex)")
    author: UserEmbedded = Field(description="Label author")
    updated_by: UserEmbedded = Field(description="User who last updated the label")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class MilestoneEmbedded(BaseModel):
    """Embedded milestone reference."""

    id: str = Field(description="Milestone ID")
    slug: str = Field(description="Milestone slug")


class PullRequestEmbedded(BaseModel):
    """Embedded pull request reference."""

    id: str = Field(description="Pull request ID")
    slug: str = Field(description="Pull request slug")


class ReactionCount(BaseModel):
    """Reaction count model."""

    count: int = Field(description="Number of reactions")


class AttachmentEmbedded(BaseModel):
    """Embedded attachment reference."""

    id: str = Field(description="Attachment ID")
    name: str = Field(description="Attachment name")
    url: str = Field(description="Attachment URL")


class IssueCommentEmbedded(BaseModel):
    """Embedded issue comment reference."""

    id: str = Field(description="Comment ID")


class IssueComment(BaseModel):
    """Issue comment model."""

    id: str = Field(description="Comment ID")
    body: str = Field(description="Comment body")

    # Relationships
    parent: IssueCommentEmbedded | None = Field(None, description="Parent comment")
    author: UserEmbedded = Field(description="Comment author")
    updated_by: UserEmbedded | None = Field(None, description="User who last updated")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    # Reactions
    reactions: dict[str, ReactionCount] = Field(
        default_factory=dict, description="Reactions keyed by reaction type"
    )

    # Attachments
    attachments: list[AttachmentEmbedded] = Field(
        default_factory=list, description="Attachments"
    )


class Issue(BaseModel):
    """Issue model."""

    id: str = Field(description="Issue ID")
    slug: str = Field(description="Issue slug")
    title: str = Field(description="Issue title")
    description: str | None = Field(None, description="Issue description")

    # Status and metadata
    status: IssueStatus = Field(description="Issue status")
    priority: Priority | None = Field(None, description="Issue priority")
    visibility: IssueVisibility = Field(description="Issue visibility")

    # Relationships
    author: UserEmbedded = Field(description="Issue author")
    updated_by: UserEmbedded | None = Field(None, description="User who last updated")
    assignee: UserEmbedded | None = Field(None, description="Assignee")
    labels: list[LabelEmbedded] = Field(default_factory=list, description="Labels")
    linked_prs: list[PullRequestEmbedded] = Field(
        default_factory=list, description="Linked pull requests"
    )
    milestone: MilestoneEmbedded | None = Field(None, description="Milestone")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    deadline: datetime | None = Field(None, description="User-defined deadline")
    started_at: datetime | None = Field(
        None, description="Timestamp when issue was last moved to in_progress"
    )
    completed_at: datetime | None = Field(
        None, description="Timestamp when issue was last moved to completed or canceled"
    )


class IssueEvent(BaseModel):
    """Issue event model."""

    id: str = Field(description="Event ID")
    event: str = Field(description="Event type")
    actor: UserEmbedded = Field(description="User who triggered the event")
    created_at: datetime = Field(description="Event timestamp")
    label: LabelEmbedded | None = Field(None, description="Label (if applicable)")
    assignee: UserEmbedded | None = Field(None, description="Assignee (if applicable)")
    milestone: MilestoneEmbedded | None = Field(
        None, description="Milestone (if applicable)"
    )


class CreateIssueRequest(BaseModel):
    """Request to create an issue."""

    title: str = Field(min_length=1, max_length=256, description="Issue title")
    body: str | None = Field(None, description="Issue body")
    assignee_ids: list[str] | None = Field(None, description="User IDs to assign")
    label_ids: list[str] | None = Field(None, description="Label IDs to add")
    milestone_id: str | None = Field(None, description="Milestone ID")


class UpdateIssueRequest(BaseModel):
    """Request to update an issue."""

    title: str | None = Field(
        None, min_length=1, max_length=256, description="Issue title"
    )
    body: str | None = Field(None, description="Issue body")
    state: str | None = Field(None, description="Issue state")  # Deprecated, use status
    state_reason: str | None = Field(None, description="State reason")  # Deprecated
    assignee_ids: list[str] | None = Field(None, description="User IDs to assign")
    label_ids: list[str] | None = Field(None, description="Label IDs (replaces all)")
    milestone_id: str | None = Field(None, description="Milestone ID")


class IssueFilters(BaseModel):
    """Filters for listing issues."""

    state: str | None = Field(None, description="Filter by state (deprecated)")
    assignee_id: str | None = Field(None, description="Filter by assignee")
    creator_id: str | None = Field(None, description="Filter by creator")
    label_ids: list[str] | None = Field(None, description="Filter by labels")
    milestone_id: str | None = Field(None, description="Filter by milestone")
