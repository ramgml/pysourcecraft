"""Pydantic models for CI/CD."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel


# =============================================================================
# Enums
# =============================================================================


class WorkflowState(str, Enum):
    """Workflow run state enum."""

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    WAITING = "waiting"
    PENDING = "pending"


class WorkflowConclusion(str, Enum):
    """Workflow run conclusion enum."""

    SUCCESS = "success"
    FAILURE = "failure"
    NEUTRAL = "neutral"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"
    TIMED_OUT = "timed_out"
    ACTION_REQUIRED = "action_required"


class WorkflowEvent(str, Enum):
    """Workflow trigger event enum."""

    PUSH = "push"
    PULL_REQUEST = "pull_request"
    PULL_REQUEST_TARGET = "pull_request_target"
    WORKFLOW_DISPATCH = "workflow_dispatch"
    SCHEDULE = "schedule"
    RELEASE = "release"
    ISSUE_COMMENT = "issue_comment"


class PipelineStatus(str, Enum):
    """Pipeline status enum."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"
    SKIPPED = "skipped"


class RunStatus(str, Enum):
    """CI/CD run status enum (from swagger)."""

    CREATED = "created"
    PREPARED = "prepared"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"
    TIMEOUT = "timeout"


class ArtifactStatus(str, Enum):
    """Artifact status enum (from swagger)."""

    REGISTERED = "registered"
    SUCCESS = "success"
    FAILED = "failed"
    MISSING = "missing"


# =============================================================================
# Supporting Models
# =============================================================================


class DatesByStage(BaseModel):
    """Dates for CI/CD entities by stage (from swagger)."""

    created_at: datetime | None = Field(None, description="Creation timestamp")
    started_at: datetime | None = Field(None, description="Start timestamp")
    finished_at: datetime | None = Field(None, description="Finish timestamp")
    updated_at: datetime | None = Field(None, description="Last update timestamp")


class ArtifactDates(BaseModel):
    """Dates for artifacts (from swagger)."""

    registered_at: datetime | None = Field(None, description="Registration timestamp")
    obtained_at: datetime | None = Field(None, description="Acquisition timestamp")
    updated_at: datetime | None = Field(None, description="Last update timestamp")


class Dependency(BaseModel):
    """Dependency reference (from swagger)."""

    name: str = Field(description="Dependency name")


class Relations(BaseModel):
    """Entity relations (from swagger)."""

    needs: list[Dependency] = Field(default_factory=list, description="Dependencies")


# =============================================================================
# Main CI/CD Models (Swagger-Compliant)
# =============================================================================


class Artifact(BaseModel):
    """CI/CD artifact model (matches swagger schema).

    Note: This model has been updated to match the swagger schema.
    The swagger Artifact has: id, local_path, dates, status, download_url
    """

    id: str = Field(description="Artifact ID")
    local_path: str = Field(description="Local path as defined in CI config")
    dates: ArtifactDates = Field(description="Artifact dates")
    status: ArtifactStatus = Field(description="Artifact status")
    download_url: str = Field(description="Temporary download URL")


class Cube(BaseModel):
    """Cube model - execution unit within a task (from swagger)."""

    id: str = Field(description="Cube ID")
    slug: str = Field(description="Cube name as defined in config")
    dates: DatesByStage = Field(description="Cube dates")
    status: RunStatus = Field(description="Cube status")
    artifacts: list[Artifact] = Field(
        default_factory=list, description="Cube artifacts"
    )
    relations: Relations | None = Field(None, description="Cube relations")


class Task(BaseModel):
    """Task model - unit of work within a workflow (from swagger)."""

    id: str = Field(description="Task ID")
    slug: str = Field(description="Task name as defined in config")
    description: str | None = Field(None, description="Task description")
    dates: DatesByStage = Field(description="Task dates")
    status: RunStatus = Field(description="Task status")
    cubes: list[Cube] = Field(default_factory=list, description="Task cubes")
    progress: dict | None = Field(None, description="Task progress")
    relations: Relations | None = Field(None, description="Task relations")


class CIWorkflow(BaseModel):
    """CI/CD Workflow model (matches swagger schema for Run workflows).

    Note: This is the swagger-compliant Workflow used within Run entities.
    It has: id, slug, description, dates, status, tasks, progress
    """

    id: str = Field(description="Workflow ID")
    slug: str = Field(description="Workflow name as defined in config")
    description: str | None = Field(None, description="Workflow description")
    dates: DatesByStage = Field(description="Workflow dates")
    status: RunStatus = Field(description="Workflow status")
    tasks: list[Task] = Field(default_factory=list, description="Workflow tasks")
    progress: dict | None = Field(None, description="Workflow progress")


class Workflow(BaseModel):
    """Workflow definition model (GitHub-style, for repository workflows).

    Note: This model is used for the /repos/{owner}/{repo}/workflows endpoint
    which returns GitHub-style workflow definitions, not CI run workflows.
    """

    id: str = Field(description="Workflow ID")
    name: str = Field(description="Workflow name")
    path: str = Field(description="File path")
    state: str = Field(description="Workflow state (active/disabled)")
    url: str = Field(description="API URL")
    html_url: str = Field(description="HTML URL")
    badge_url: str | None = Field(None, description="Status badge URL")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class Run(BaseModel):
    """Run model - main CI/CD run entity (from swagger).

    This is the primary CI/CD entity that contains workflows.
    """

    id: str = Field(description="Run ID")
    slug: str = Field(description="Run counter as slug")
    dates: DatesByStage = Field(description="Run dates")
    status: RunStatus = Field(description="Run status")
    workflows: list[CIWorkflow] = Field(
        default_factory=list, description="Run workflows"
    )
    event_type: str | None = Field(None, description="Event that triggered this run")
    error_messages: list[str] = Field(
        default_factory=list, description="Error messages"
    )
    pull: dict | None = Field(None, description="Pull request that triggered this run")
    user: dict | None = Field(None, description="User that triggered this run")


# =============================================================================
# Legacy Models (for backward compatibility)
# =============================================================================


class WorkflowRun(BaseModel):
    """Workflow run model (GitHub-style, legacy).

    Note: This model is maintained for backward compatibility.
    The swagger schema uses Run as the main CI/CD entity.
    """

    id: str = Field(description="Run ID")
    name: str = Field(description="Workflow name")
    run_number: int = Field(description="Run number")
    run_attempt: int = Field(default=1, ge=1, description="Attempt number")
    url: str = Field(description="API URL")
    html_url: str = Field(description="HTML URL")

    # Status
    state: WorkflowState = Field(description="Run state")
    conclusion: WorkflowConclusion | None = Field(None, description="Run conclusion")

    # Trigger
    event: WorkflowEvent = Field(description="Trigger event")
    head_branch: str | None = Field(None, description="Branch name")
    head_sha: str = Field(description="Commit SHA")
    head_commit_message: str | None = Field(None, description="Commit message")

    # Actor
    actor_id: str = Field(description="Actor user ID")
    actor_username: str = Field(description="Actor username")
    triggering_actor_id: str | None = Field(None, description="Triggering actor ID")
    triggering_actor_username: str | None = Field(
        None, description="Triggering actor username"
    )

    # Repository
    repository_id: str = Field(description="Repository ID")
    repository_name: str = Field(description="Repository name")

    # Pull Request
    pull_request_number: int | None = Field(None, description="Related PR number")
    pull_request_url: str | None = Field(None, description="Related PR URL")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    run_started_at: datetime | None = Field(None, description="Run start timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")

    # Duration (in seconds)
    duration_seconds: int | None = Field(None, ge=0, description="Run duration")

    # URLs
    jobs_url: str = Field(description="Jobs API URL")
    logs_url: str | None = Field(None, description="Logs URL")
    check_suite_url: str | None = Field(None, description="Check suite URL")
    artifacts_url: str = Field(description="Artifacts API URL")
    cancel_url: str = Field(description="Cancel API URL")
    rerun_url: str = Field(description="Rerun API URL")

    # Stats
    jobs_count: int = Field(default=0, ge=0, description="Total jobs")
    jobs_completed: int = Field(default=0, ge=0, description="Completed jobs")
    jobs_failed: int = Field(default=0, ge=0, description="Failed jobs")

    # Metadata
    path: str = Field(description="Workflow file path")
    display_title: str = Field(description="Display title")


class WorkflowJobStep(BaseModel):
    """Workflow job step model (legacy)."""

    name: str = Field(description="Step name")
    state: WorkflowState = Field(description="Step state")
    conclusion: WorkflowConclusion | None = Field(None, description="Step conclusion")
    number: int = Field(description="Step number")
    started_at: datetime | None = Field(None, description="Start timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")
    duration_seconds: int | None = Field(None, ge=0, description="Step duration")


class WorkflowJob(BaseModel):
    """Workflow job model (legacy)."""

    id: str = Field(description="Job ID")
    run_id: str = Field(description="Workflow run ID")
    run_url: str = Field(description="Run API URL")
    name: str = Field(description="Job name")
    url: str = Field(description="API URL")
    html_url: str | None = Field(None, description="HTML URL")

    # Status
    state: WorkflowState = Field(description="Job state")
    conclusion: WorkflowConclusion | None = Field(None, description="Job conclusion")

    # Runner
    runner_id: str | None = Field(None, description="Runner ID")
    runner_name: str | None = Field(None, description="Runner name")
    runner_group_id: str | None = Field(None, description="Runner group ID")
    runner_group_name: str | None = Field(None, description="Runner group name")

    # Steps
    steps: list[WorkflowJobStep] = Field(default_factory=list, description="Job steps")

    # Labels
    labels: list[str] = Field(default_factory=list, description="Runner labels")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    started_at: datetime | None = Field(None, description="Start timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")


class PipelineStage(BaseModel):
    """Pipeline stage model (legacy)."""

    id: str = Field(description="Stage ID")
    name: str = Field(description="Stage name")
    status: PipelineStatus = Field(description="Stage status")
    jobs: list[PipelineJob] = Field(default_factory=list, description="Stage jobs")
    created_at: datetime = Field(description="Creation timestamp")
    started_at: datetime | None = Field(None, description="Start timestamp")
    finished_at: datetime | None = Field(None, description="Finish timestamp")
    duration_seconds: int | None = Field(None, ge=0, description="Duration")


class PipelineJob(BaseModel):
    """Pipeline job model (legacy)."""

    id: str = Field(description="Job ID")
    name: str = Field(description="Job name")
    status: PipelineStatus = Field(description="Job status")
    stage: str = Field(description="Stage name")
    url: str = Field(description="API URL")
    web_url: str = Field(description="Web URL")

    # Runner
    runner_id: str | None = Field(None, description="Runner ID")
    runner_name: str | None = Field(None, description="Runner name")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    started_at: datetime | None = Field(None, description="Start timestamp")
    finished_at: datetime | None = Field(None, description="Finish timestamp")
    duration_seconds: int | None = Field(None, ge=0, description="Duration")

    # Artifacts - using legacy format for backward compatibility
    artifacts: list[LegacyArtifact] = Field(
        default_factory=list, description="Job artifacts"
    )

    # Coverage
    coverage: float | None = Field(None, ge=0, le=100, description="Test coverage")

    # Failure
    failure_reason: str | None = Field(None, description="Failure reason")
    allow_failure: bool = Field(default=False, description="Allowed to fail")


class LegacyArtifact(BaseModel):
    """Legacy artifact model (GitHub-style, for backward compatibility).

    Note: This is the old artifact format. New code should use Artifact.
    """

    id: str = Field(description="Artifact ID")
    name: str = Field(description="Artifact name")
    size_in_bytes: int = Field(ge=0, description="Size in bytes")
    url: str = Field(description="API URL")
    archive_download_url: str = Field(description="Download URL")
    expired: bool = Field(default=False, description="Whether artifact expired")
    expires_at: datetime | None = Field(None, description="Expiration timestamp")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class Pipeline(BaseModel):
    """Pipeline model (legacy).

    Note: This model is NOT in the swagger schema. The swagger schema
    uses Run as the main CI/CD entity. This is maintained for backward
    compatibility with existing endpoints.
    """

    id: str = Field(description="Pipeline ID")
    name: str = Field(description="Pipeline name")
    status: PipelineStatus = Field(description="Pipeline status")
    url: str = Field(description="API URL")
    web_url: str = Field(description="Web URL")

    # Repository
    repository_id: str = Field(description="Repository ID")
    ref: str = Field(description="Git ref (branch/tag)")
    sha: str = Field(description="Commit SHA")

    # Trigger
    source: str = Field(description="Pipeline source")
    trigger_id: str | None = Field(None, description="Trigger user ID")
    trigger_username: str | None = Field(None, description="Trigger username")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    started_at: datetime | None = Field(None, description="Start timestamp")
    finished_at: datetime | None = Field(None, description="Finish timestamp")
    duration_seconds: int | None = Field(None, ge=0, description="Duration")

    # Stages
    stages: list[PipelineStage] = Field(
        default_factory=list, description="Pipeline stages"
    )

    # Coverage
    coverage: float | None = Field(
        None, ge=0, le=100, description="Test coverage percentage"
    )
