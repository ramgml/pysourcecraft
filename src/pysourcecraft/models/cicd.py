"""Pydantic models for CI/CD."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel


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


class WorkflowRun(BaseModel):
    """Workflow run model."""

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
    triggering_actor_username: str | None = Field(None, description="Triggering actor username")

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


class WorkflowJob(BaseModel):
    """Workflow job model."""

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


class WorkflowJobStep(BaseModel):
    """Workflow job step model."""

    name: str = Field(description="Step name")
    state: WorkflowState = Field(description="Step state")
    conclusion: WorkflowConclusion | None = Field(None, description="Step conclusion")
    number: int = Field(description="Step number")
    started_at: datetime | None = Field(None, description="Start timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")
    duration_seconds: int | None = Field(None, ge=0, description="Step duration")


class Workflow(BaseModel):
    """Workflow definition model."""

    id: str = Field(description="Workflow ID")
    name: str = Field(description="Workflow name")
    path: str = Field(description="File path")
    state: str = Field(description="Workflow state (active/disabled)")
    url: str = Field(description="API URL")
    html_url: str = Field(description="HTML URL")
    badge_url: str | None = Field(None, description="Status badge URL")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class Pipeline(BaseModel):
    """Pipeline model (CI/CD pipeline)."""

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
    stages: list[PipelineStage] = Field(default_factory=list, description="Pipeline stages")

    # Coverage
    coverage: float | None = Field(None, ge=0, le=100, description="Test coverage percentage")


class PipelineStage(BaseModel):
    """Pipeline stage model."""

    id: str = Field(description="Stage ID")
    name: str = Field(description="Stage name")
    status: PipelineStatus = Field(description="Stage status")
    jobs: list[PipelineJob] = Field(default_factory=list, description="Stage jobs")
    created_at: datetime = Field(description="Creation timestamp")
    started_at: datetime | None = Field(None, description="Start timestamp")
    finished_at: datetime | None = Field(None, description="Finish timestamp")
    duration_seconds: int | None = Field(None, ge=0, description="Duration")


class PipelineJob(BaseModel):
    """Pipeline job model."""

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

    # Artifacts
    artifacts: list[Artifact] = Field(default_factory=list, description="Job artifacts")

    # Coverage
    coverage: float | None = Field(None, ge=0, le=100, description="Test coverage")

    # Failure
    failure_reason: str | None = Field(None, description="Failure reason")
    allow_failure: bool = Field(default=False, description="Allowed to fail")


class Artifact(BaseModel):
    """CI/CD artifact model."""

    id: str = Field(description="Artifact ID")
    name: str = Field(description="Artifact name")
    size_in_bytes: int = Field(ge=0, description="Size in bytes")
    url: str = Field(description="API URL")
    archive_download_url: str = Field(description="Download URL")
    expired: bool = Field(default=False, description="Whether artifact expired")
    expires_at: datetime | None = Field(None, description="Expiration timestamp")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")