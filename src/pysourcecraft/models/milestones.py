"""Pydantic models for Milestones.

Matches swagger schema definitions for Milestone-related models.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel
from pysourcecraft.models.users import UserEmbedded


class MilestoneStatus(str, Enum):
    """Milestone status enum.

    Matches swagger schema Milestone.Status definition.
    """

    OPEN = "open"
    CLOSED = "closed"


class MilestoneEmbedded(BaseModel):
    """Minimal milestone reference (embedded in other models).

    Matches swagger schema MilestoneEmbedded definition.
    """

    id: str = Field(description="Milestone ID")
    slug: str = Field(description="Milestone slug")


class Milestone(BaseModel):
    """Milestone model.

    Matches swagger schema Milestone definition.
    """

    id: str = Field(description="Milestone ID")
    name: str = Field(description="Milestone name")
    slug: str = Field(description="Milestone slug")
    description: str | None = Field(None, description="Milestone description")
    start_date: datetime | None = Field(None, description="Milestone start date")
    deadline: datetime | None = Field(None, description="Milestone deadline (end date)")
    status: MilestoneStatus = Field(description="Milestone status")

    # Authors
    author: UserEmbedded = Field(description="Milestone creator")
    updated_by: UserEmbedded | None = Field(None, description="User who last updated")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    # Backward compatibility property
    @property
    def title(self) -> str:
        """Backward compatibility: returns name as title."""
        return self.name

    @property
    def state(self) -> MilestoneStatus:
        """Backward compatibility: returns status as state."""
        return self.status

    @property
    def due_on(self) -> datetime | None:
        """Backward compatibility: returns deadline as due_on."""
        return self.deadline


# Backward compatibility alias
MilestoneState = MilestoneStatus


class CreateMilestoneRequest(BaseModel):
    """Request to create a milestone.

    Matches swagger schema CreateMilestoneBody definition.
    """

    name: str = Field(min_length=1, description="Milestone name")
    slug: str | None = Field(
        None, description="Optional slug (auto-generated from name if not provided)"
    )
    description: str | None = Field(None, description="Milestone description")
    start_date: datetime | None = Field(None, description="Milestone start date")
    deadline: datetime | None = Field(None, description="Milestone deadline (end date)")


class UpdateMilestoneRequest(BaseModel):
    """Request to update a milestone.

    Matches swagger schema UpdateMilestoneBody definition.
    """

    name: str | None = Field(None, description="Milestone name")
    slug: str | None = Field(None, description="Milestone slug")
    description: str | None = Field(None, description="Milestone description")
    start_date: datetime | None = Field(None, description="Milestone start date")
    deadline: datetime | None = Field(None, description="Milestone deadline (end date)")
    status: MilestoneStatus | None = Field(None, description="Milestone status")
