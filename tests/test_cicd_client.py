"""Integration tests for the CICDClient."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import (
    LegacyArtifact,
    PaginatedResponse,
    Pipeline,
    PipelineStatus,
    Workflow,
    WorkflowRun,
    WorkflowState,
    WorkflowConclusion,
)

from tests.conftest import create_paginated_response


class TestCICDClientWorkflows:
    """Tests for workflow operations."""

    @pytest.mark.asyncio
    async def test_list_workflows(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test listing workflows in a repository."""
        workflow_data = {
            "id": "workflow-001",
            "name": "CI",
            "path": ".github/workflows/ci.yml",
            "state": "active",
            "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/workflows/1",
            "html_url": "https://sourcecraft.dev/testuser/test-repo/blob/main/.github/workflows/ci.yml",
            "badge_url": "https://sourcecraft.dev/testuser/test-repo/workflows/CI/badge.svg",
            "created_at": mock_datetime.isoformat(),
            "updated_at": mock_datetime.isoformat(),
        }
        response_data = create_paginated_response([workflow_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/workflows"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.cicd.list_workflows("testuser", "test-repo")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].name == "CI"
        assert result.data[0].state == "active"

    @pytest.mark.asyncio
    async def test_get_workflow(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test getting a single workflow."""
        workflow_data = {
            "id": "workflow-001",
            "name": "CI",
            "path": ".github/workflows/ci.yml",
            "state": "active",
            "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/workflows/1",
            "html_url": "https://sourcecraft.dev/testuser/test-repo/blob/main/.github/workflows/ci.yml",
            "badge_url": "https://sourcecraft.dev/testuser/test-repo/workflows/CI/badge.svg",
            "created_at": mock_datetime.isoformat(),
            "updated_at": mock_datetime.isoformat(),
        }
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/workflows/workflow-001"
        ).mock(return_value=Response(200, json=workflow_data))

        result = await client.cicd.get_workflow("testuser", "test-repo", "workflow-001")

        assert isinstance(result, Workflow)
        assert result.id == "workflow-001"
        assert result.name == "CI"


class TestCICDClientWorkflowRuns:
    """Tests for workflow run operations."""

    @pytest.mark.asyncio
    async def test_list_workflow_runs(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_workflow_run_data: dict[str, Any],
    ) -> None:
        """Test listing workflow runs."""
        response_data = create_paginated_response([mock_workflow_run_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.cicd.list_workflow_runs("testuser", "test-repo")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].name == "CI"

    @pytest.mark.asyncio
    async def test_list_workflow_runs_for_workflow(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_workflow_run_data: dict[str, Any],
    ) -> None:
        """Test listing runs for a specific workflow."""
        response_data = create_paginated_response([mock_workflow_run_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/workflows/workflow-001/runs"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.cicd.list_workflow_runs(
            "testuser", "test-repo", workflow_id="workflow-001"
        )

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_list_workflow_runs_with_branch_filter(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_workflow_run_data: dict[str, Any],
    ) -> None:
        """Test listing workflow runs filtered by branch."""
        response_data = create_paginated_response([mock_workflow_run_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.cicd.list_workflow_runs(
            "testuser", "test-repo", branch="main"
        )

        assert isinstance(result, PaginatedResponse)

    @pytest.mark.asyncio
    async def test_get_workflow_run(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_workflow_run_data: dict[str, Any],
    ) -> None:
        """Test getting a single workflow run."""
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs/run-001"
        ).mock(return_value=Response(200, json=mock_workflow_run_data))

        result = await client.cicd.get_workflow_run("testuser", "test-repo", "run-001")

        assert isinstance(result, WorkflowRun)
        assert result.id == "run-001"
        assert result.state == WorkflowState.COMPLETED
        assert result.conclusion == WorkflowConclusion.SUCCESS

    @pytest.mark.asyncio
    async def test_cancel_workflow_run(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test canceling a workflow run."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs/run-001/cancel"
        ).mock(return_value=Response(202, json={}))

        result = await client.cicd.cancel_workflow_run(
            "testuser", "test-repo", "run-001"
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_rerun_workflow_run(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test re-running a workflow run."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs/run-001/rerun"
        ).mock(return_value=Response(201, json={}))

        result = await client.cicd.rerun_workflow_run(
            "testuser", "test-repo", "run-001"
        )

        assert result is None


class TestCICDClientPipelines:
    """Tests for pipeline operations."""

    @pytest.mark.asyncio
    async def test_list_pipelines(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pipeline_data: dict[str, Any],
    ) -> None:
        """Test listing pipelines."""
        response_data = create_paginated_response([mock_pipeline_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pipelines"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.cicd.list_pipelines("testuser", "test-repo")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].name == "Test Pipeline"

    @pytest.mark.asyncio
    async def test_get_pipeline(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pipeline_data: dict[str, Any],
    ) -> None:
        """Test getting a single pipeline."""
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pipelines/pipeline-001"
        ).mock(return_value=Response(200, json=mock_pipeline_data))

        result = await client.cicd.get_pipeline("testuser", "test-repo", "pipeline-001")

        assert isinstance(result, Pipeline)
        assert result.id == "pipeline-001"
        assert result.status == PipelineStatus.SUCCESS

    @pytest.mark.asyncio
    async def test_create_pipeline(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pipeline_data: dict[str, Any],
    ) -> None:
        """Test creating a new pipeline."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pipelines"
        ).mock(return_value=Response(201, json=mock_pipeline_data))

        result = await client.cicd.create_pipeline("testuser", "test-repo", "main")

        assert isinstance(result, Pipeline)
        assert result.ref == "main"

    @pytest.mark.asyncio
    async def test_create_pipeline_with_variables(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pipeline_data: dict[str, Any],
    ) -> None:
        """Test creating a pipeline with variables."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pipelines"
        ).mock(return_value=Response(201, json=mock_pipeline_data))

        variables = {"DEPLOY_ENV": "staging", "VERSION": "1.0.0"}
        await client.cicd.create_pipeline("testuser", "test-repo", "main", variables)

    @pytest.mark.asyncio
    async def test_retry_pipeline(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pipeline_data: dict[str, Any],
    ) -> None:
        """Test retrying a failed pipeline."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pipelines/pipeline-001/retry"
        ).mock(return_value=Response(201, json=mock_pipeline_data))

        result = await client.cicd.retry_pipeline(
            "testuser", "test-repo", "pipeline-001"
        )

        assert isinstance(result, Pipeline)

    @pytest.mark.asyncio
    async def test_cancel_pipeline(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_pipeline_data: dict[str, Any],
    ) -> None:
        """Test canceling a pipeline."""
        mock_router.post(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/pipelines/pipeline-001/cancel"
        ).mock(return_value=Response(202, json=mock_pipeline_data))

        result = await client.cicd.cancel_pipeline(
            "testuser", "test-repo", "pipeline-001"
        )

        assert isinstance(result, Pipeline)


class TestCICDClientArtifacts:
    """Tests for artifact operations."""

    @pytest.mark.asyncio
    async def test_list_artifacts(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test listing artifacts for a run."""
        artifact_data = {
            "id": "artifact-001",
            "name": "test-results",
            "size_in_bytes": 1024000,
            "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/artifacts/1",
            "archive_download_url": "https://sourcecraft.dev/testuser/test-repo/suites/1/artifacts/test-results.zip",
            "expired": False,
            "expires_at": None,
            "created_at": mock_datetime.isoformat(),
            "updated_at": mock_datetime.isoformat(),
        }
        response_data = create_paginated_response([artifact_data], total=1)
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/runs/run-001/artifacts"
        ).mock(return_value=Response(200, json=response_data))

        result = await client.cicd.list_artifacts("testuser", "test-repo", "run-001")

        assert isinstance(result, PaginatedResponse)
        assert len(result.data) == 1
        assert result.data[0].name == "test-results"

    @pytest.mark.asyncio
    async def test_get_artifact(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_datetime: Any,
    ) -> None:
        """Test getting a single artifact."""
        artifact_data = {
            "id": "artifact-001",
            "name": "test-results",
            "size_in_bytes": 1024000,
            "url": "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/artifacts/1",
            "archive_download_url": "https://sourcecraft.dev/testuser/test-repo/suites/1/artifacts/test-results.zip",
            "expired": False,
            "expires_at": None,
            "created_at": mock_datetime.isoformat(),
            "updated_at": mock_datetime.isoformat(),
        }
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/artifacts/artifact-001"
        ).mock(return_value=Response(200, json=artifact_data))

        result = await client.cicd.get_artifact("testuser", "test-repo", "artifact-001")

        assert isinstance(result, LegacyArtifact)
        assert result.id == "artifact-001"

    @pytest.mark.asyncio
    async def test_delete_artifact(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test deleting an artifact."""
        mock_router.delete(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/artifacts/artifact-001"
        ).mock(return_value=Response(204, json={}))

        result = await client.cicd.delete_artifact(
            "testuser", "test-repo", "artifact-001"
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_download_artifact(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test downloading an artifact."""
        artifact_content = b"PK\x03\x04\x14\x00\x00\x00\x08\x00"  # ZIP file header
        mock_router.get(
            "https://api.sourcecraft.dev/v1/repos/testuser/test-repo/actions/artifacts/artifact-001/zip"
        ).mock(return_value=Response(200, content=artifact_content))

        result = await client.cicd.download_artifact(
            "testuser", "test-repo", "artifact-001"
        )

        assert result == artifact_content
