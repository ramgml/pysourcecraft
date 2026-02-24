"""Pydantic models for Milestones."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel


class MilestoneState(str, Enum):
    """Milestone state enum."""

    OPEN = "open"
    CLOSED = "closed"


class Milestone(BaseModel):
    """Milestone model."""

    id: str = Field(description="Milestone ID")
    number: int = Field(description="Milestone number")
    title: str = Field(description="Milestone title")
    description: str | None = Field(None, description="Milestone description")
    state: MilestoneState = Field(description="Milestone state")
    url: str = Field(description="API URL")
    html_url: str = Field(description="HTML URL")

    # Creator
    creator_id: str = Field(description="Creator user ID")
    creator_username: str = Field(description="Creator username")

    # Due date
    due_on: datetime | None = Field(None, description="Due date")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    closed_at: datetime | None = Field(None, description="Closed timestamp")

    # Progress
    open_issues_count: int = Field(default=0, ge=0, description="Open issues count")
    closed_issues_count: int = Field(default=0, ge=0, description="Closed issues count")

    @property
    def total_issues(self) -> int:
        """Total number of issues."""
        return self.open_issues_count + self.closed_issues_count

    @property
    def progress_percentage(self) -> float:
        """Completion percentage."""
        total = self.total_issues
        if total == 0:
            return 0.0
        return (self.closed_issues_count / total) * 100


class CreateMilestoneRequest(BaseModel):
    """Request to create a milestone."""

    title: str = Field(min_length=1, max_length=255, description="Milestone title")
    description: str | None = Field(None, description="Milestone description")
    state: MilestoneState = Field(default=MilestoneState.OPEN, description="Milestone state")
    due_on: datetime | None = Field(None, description="Due date")


class UpdateMilestoneRequest(BaseModel):
    """Request to update a milestone."""

    title: str | None = Field(None, min_length=1, max_length=255, description="Milestone title")
    description: str | None = Field(None, description="Milestone description")
    state: MilestoneState | None = Field(None, description="Milestone state")
    due_on: datetime | None = Field(None, description="Due date")