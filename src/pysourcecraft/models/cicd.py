"""Pydantic models for CI/CD."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel
from pysourcecraft.models.issues import PullRequestEmbedded, UserEmbedded


# =============================================================================
# Enums (sourcecraft.swagger.json)
# =============================================================================


class RunStatus(str, Enum):
    """CI/CD run/workflow/task/cube status enum (swagger `Run.Status`)."""

    CREATED = "created"
    PREPARED = "prepared"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"
    TIMEOUT = "timeout"


class EventType(str, Enum):
    """Event that triggered a run (swagger `EventType`)."""

    PUSH = "push"
    PR_UPDATE = "pr_update"
    MANUAL = "manual"
    RESTART = "restart"


class ArtifactStatus(str, Enum):
    """Artifact status enum (swagger `ArtifactStatus`)."""

    REGISTERED = "registered"
    SUCCESS = "success"
    FAILED = "failed"
    MISSING = "missing"


# =============================================================================
# Supporting Models
# =============================================================================


class DatesByStage(BaseModel):
    """Dates for CI/CD entities by stage (swagger `DatesByStage`)."""

    created_at: datetime | None = Field(None, description="Creation timestamp")
    started_at: datetime | None = Field(None, description="Start timestamp")
    finished_at: datetime | None = Field(None, description="Finish timestamp")
    updated_at: datetime | None = Field(None, description="Last update timestamp")


class ArtifactDates(BaseModel):
    """Dates for artifacts (swagger `ArtifactDates`)."""

    registered_at: datetime | None = Field(None, description="Registration timestamp")
    obtained_at: datetime | None = Field(None, description="Acquisition timestamp")
    updated_at: datetime | None = Field(None, description="Last update timestamp")


class Dependency(BaseModel):
    """Dependency reference (swagger `Dependency`)."""

    name: str = Field(description="Dependency name")


class Relations(BaseModel):
    """Entity relations (swagger `Relations`)."""

    needs: list[Dependency] = Field(default_factory=list, description="Dependencies")


class Progress(BaseModel):
    """Execution progress (swagger `Progress`)."""

    percent: float | None = Field(None, description="Completion percent (0..1)")
    current_cube: Cube | None = Field(
        None, description="Cube currently being executed (any of concurrently running)"
    )


class GitRevision(BaseModel):
    """Git revision — exactly one field must be provided (swagger `GitRevision`)."""

    branch: str | None = Field(None, description="Branch name")
    tag: str | None = Field(None, description="Tag name")
    commit: str | None = Field(None, description="Commit hash")


class InputValue(BaseModel):
    """Workflow input parameter (swagger `InputValue`)."""

    name: str = Field(description="Input name")
    value: str = Field(description="Input value")


class WorkflowData(BaseModel):
    """Which workflow to run (swagger `WorkflowData`)."""

    name: str = Field(description="Workflow name as defined in the config")
    values: list[InputValue] = Field(
        default_factory=list, description="Input parameters to pass to the workflow"
    )


class RunWorkflowsRequest(BaseModel):
    """Body for POST /repos/{org}/{repo}/cicd/runs (swagger `RunWorkflowsBody`)."""

    head: GitRevision | None = Field(
        None,
        description="Revision to run on; empty = default branch",
    )
    config_revision: GitRevision | None = Field(
        None,
        description="Revision to fetch the CI config from; empty = default branch",
    )
    workflows: list[WorkflowData] = Field(
        default_factory=list, description="Workflows to run"
    )
    shared: bool | None = Field(
        None, description="Run shared workflows by user without repository access"
    )


# =============================================================================
# Main CI/CD Models (sourcecraft.swagger.json)
# =============================================================================


class Artifact(BaseModel):
    """CI/CD artifact (swagger `Artifact`)."""

    id: str = Field(description="Artifact ID (empty: no public IDs yet)")
    local_path: str = Field(description="Path as defined in the CI config")
    dates: ArtifactDates = Field(description="Artifact dates")
    status: ArtifactStatus = Field(description="Artifact status")
    download_url: str = Field(description="Temporary download URL (short-lived)")


class Cube(BaseModel):
    """Cube — execution unit within a task (swagger `Cube`)."""

    id: str = Field(default="", description="Cube ID (empty: no public IDs yet)")
    slug: str = Field(description="Cube name as defined in the config")
    dates: DatesByStage = Field(default_factory=DatesByStage, description="Cube dates")
    status: RunStatus = Field(description="Cube status")
    artifacts: list[Artifact] = Field(
        default_factory=list, description="Cube artifacts"
    )
    relations: Relations | None = Field(None, description="Cube relations")


class Task(BaseModel):
    """Task — unit of work within a workflow (swagger `Task`)."""

    id: str = Field(default="", description="Task ID (empty: no public IDs yet)")
    slug: str = Field(description="Task name as defined in the config")
    description: str | None = Field(None, description="Task description")
    dates: DatesByStage = Field(default_factory=DatesByStage, description="Task dates")
    status: RunStatus = Field(description="Task status")
    cubes: list[Cube] = Field(default_factory=list, description="Task cubes")
    progress: Progress | None = Field(None, description="Task progress")
    relations: Relations | None = Field(None, description="Task relations")


class CIWorkflow(BaseModel):
    """Workflow launch within a run (swagger `Workflow`)."""

    id: str = Field(default="", description="Workflow ID (empty: no public IDs yet)")
    slug: str = Field(description="Workflow name as defined in the config")
    description: str | None = Field(None, description="Workflow description")
    dates: DatesByStage = Field(
        default_factory=DatesByStage, description="Workflow dates"
    )
    status: RunStatus = Field(description="Workflow status")
    tasks: list[Task] = Field(default_factory=list, description="Workflow tasks")
    progress: Progress | None = Field(None, description="Workflow progress")


class Run(BaseModel):
    """CI/CD run — may contain several workflow launches (swagger `Run`)."""

    id: str = Field(default="", description="Run ID (empty: no public IDs yet)")
    slug: str = Field(description="Run counter serves as a slug")
    dates: DatesByStage = Field(default_factory=DatesByStage, description="Run dates")
    status: RunStatus = Field(description="Run status")
    workflows: list[CIWorkflow] = Field(
        default_factory=list, description="Run workflows"
    )
    event_type: EventType | None = Field(
        None, description="Event that triggered this run"
    )
    error_messages: list[str] = Field(
        default_factory=list, description="Error messages"
    )
    pull: PullRequestEmbedded | None = Field(
        None,
        description="Pull request which this run corresponds to (pr_update runs)",
    )
    user: UserEmbedded | None = Field(None, description="User that triggered this run")


class RunList(BaseModel):
    """Response for list runs (swagger `ListRunsResponse`)."""

    runs: list[Run] = Field(default_factory=list, description="List of CI/CD runs")
    next_page_token: str | None = Field(
        None,
        description="Token to retrieve the next page; None/empty = last page",
    )


class GetCubeLogsResponse(BaseModel):
    """Response for cube logs (swagger `GetCubeLogsResponse`)."""

    logs: str | None = Field(None, description="Log chunk for the requested page")
    page_complete: bool = Field(
        False,
        description=(
            "True when this log page is fully written; false pages 404 on next fetch"
        ),
    )
    done: bool = Field(
        False,
        description="True when the cube finished and no more logs will be written",
    )


class GetCubeArtifactsResponse(BaseModel):
    """Response for cube artifacts (swagger `GetCubeArtifactsResponse`)."""

    artifacts: list[Artifact] = Field(
        default_factory=list,
        description="Artifacts filtered by workflow/task/cube with temporary URLs",
    )
