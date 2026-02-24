"""Pydantic models for Issues."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel


class IssueState(str, Enum):
    """Issue state enum."""

    OPEN = "open"
    CLOSED = "closed"


class IssueStateReason(str, Enum):
    """Issue state reason enum."""

    COMPLETED = "completed"
    NOT_PLANNED = "not_planned"
    REOPENED = "reopened"


class Label(BaseModel):
    """Label model."""

    id: str = Field(description="Label ID")
    name: str = Field(description="Label name")
    color: str = Field(description="Label color (hex)")
    description: str | None = Field(None, description="Label description")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class IssueAssignee(BaseModel):
    """Issue assignee reference."""

    id: str = Field(description="User ID")
    username: str = Field(description="Username")
    avatar_url: str | None = Field(None, description="Avatar URL")


class IssueMilestone(BaseModel):
    """Issue milestone reference."""

    id: str = Field(description="Milestone ID")
    number: int = Field(description="Milestone number")
    title: str = Field(description="Milestone title")
    state: str = Field(description="Milestone state")


class IssueCreator(BaseModel):
    """Issue creator reference."""

    id: str = Field(description="User ID")
    username: str = Field(description="Username")
    avatar_url: str | None = Field(None, description="Avatar URL")


class Issue(BaseModel):
    """Issue model."""

    id: str = Field(description="Issue ID")
    number: int = Field(description="Issue number")
    title: str = Field(description="Issue title")
    body: str | None = Field(None, description="Issue body")
    state: IssueState = Field(description="Issue state")
    state_reason: IssueStateReason | None = Field(None, description="State reason")
    url: str = Field(description="Issue URL")
    html_url: str = Field(description="HTML URL")

    # Relationships
    creator: IssueCreator = Field(description="Issue creator")
    assignees: list[IssueAssignee] = Field(
        default_factory=list, description="Assignees"
    )
    labels: list[Label] = Field(default_factory=list, description="Labels")
    milestone: IssueMilestone | None = Field(None, description="Milestone")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    closed_at: datetime | None = Field(None, description="Closed timestamp")

    # Counts
    comments_count: int = Field(default=0, ge=0, description="Number of comments")

    # Metadata
    locked: bool = Field(default=False, description="Whether issue is locked")


class IssueComment(BaseModel):
    """Issue comment model."""

    id: str = Field(description="Comment ID")
    body: str = Field(description="Comment body")
    url: str = Field(description="Comment URL")
    html_url: str = Field(description="HTML URL")

    # Author
    user: IssueCreator = Field(description="Comment author")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    # Metadata
    reactions: dict[str, int] = Field(default_factory=dict, description="Reactions")


class IssueEvent(BaseModel):
    """Issue event model."""

    id: str = Field(description="Event ID")
    event: str = Field(description="Event type")
    actor: IssueCreator = Field(description="User who triggered the event")
    created_at: datetime = Field(description="Event timestamp")
    label: Label | None = Field(None, description="Label (if applicable)")
    assignee: IssueAssignee | None = Field(None, description="Assignee (if applicable)")
    milestone: IssueMilestone | None = Field(
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
    state: IssueState | None = Field(None, description="Issue state")
    state_reason: IssueStateReason | None = Field(None, description="State reason")
    assignee_ids: list[str] | None = Field(None, description="User IDs to assign")
    label_ids: list[str] | None = Field(None, description="Label IDs (replaces all)")
    milestone_id: str | None = Field(None, description="Milestone ID")


class IssueFilters(BaseModel):
    """Filters for listing issues."""

    state: IssueState | None = Field(None, description="Filter by state")
    assignee_id: str | None = Field(None, description="Filter by assignee")
    creator_id: str | None = Field(None, description="Filter by creator")
    label_ids: list[str] | None = Field(None, description="Filter by labels")
    milestone_id: str | None = Field(None, description="Filter by milestone")
