"""Integration tests for the CICDClient (swagger `/cicd/...` contract)."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import (
    CIWorkflow,
    GetCubeArtifactsResponse,
    GetCubeLogsResponse,
    GitRevision,
    Run,
    RunList,
    RunStatus,
    RunWorkflowsRequest,
    WorkflowData,
    InputValue,
)

from tests.conftest import create_error_response, create_runs_response

BASE = "https://api.sourcecraft.dev/v1"
RUNS_URL = f"{BASE}/repos/testuser/test-repo/cicd/runs"


class TestCICDClientRuns:
    """Tests for run listing and retrieval."""

    @pytest.mark.asyncio
    async def test_list_runs(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_run_data: dict[str, Any],
    ) -> None:
        """Test listing CI/CD runs."""
        route = mock_router.get(RUNS_URL).mock(
            return_value=Response(200, json=create_runs_response([mock_run_data]))
        )

        result = await client.cicd.list_runs("testuser", "test-repo")

        assert route.called
        request = route.calls.last.request
        assert "page_size=30" in str(request.url)
        assert "page_token" not in str(request.url)
        assert isinstance(result, RunList)
        assert result.next_page_token is None
        assert len(result.runs) == 1
        run = result.runs[0]
        assert isinstance(run, Run)
        assert run.slug == "12"
        assert run.status == RunStatus.SUCCESS
        assert run.event_type == "push"
        assert run.user is not None and run.user.slug == "testuser"

    @pytest.mark.asyncio
    async def test_list_runs_pagination(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_run_data: dict[str, Any],
    ) -> None:
        """Test page_size/page_token query params are forwarded to the server."""
        route = mock_router.get(RUNS_URL).mock(
            return_value=Response(
                200,
                json=create_runs_response(
                    [mock_run_data], next_page_token="eyJvZmZzZXQi"
                ),
            )
        )

        result = await client.cicd.list_runs(
            "testuser", "test-repo", page_size=5, page_token="abc123"
        )

        request = route.calls.last.request
        assert "page_size=5" in str(request.url)
        assert "page_token=abc123" in str(request.url)
        assert result.next_page_token == "eyJvZmZzZXQi"

    @pytest.mark.asyncio
    async def test_get_run(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_run_data: dict[str, Any],
    ) -> None:
        """Test getting a single run with nested workflows/tasks/cubes."""
        route = mock_router.get(f"{RUNS_URL}/12").mock(
            return_value=Response(200, json=mock_run_data)
        )

        run = await client.cicd.get_run("testuser", "test-repo", "12")

        assert route.called
        assert isinstance(run, Run)
        assert run.slug == "12"
        wf = run.workflows[0]
        assert isinstance(wf, CIWorkflow)
        assert wf.slug == "ci"
        task = wf.tasks[0]
        assert task.slug == "build"
        cube = task.cubes[0]
        assert cube.slug == "package"
        assert cube.artifacts[0].local_path == "dist/app.whl"
        assert wf.progress is not None and wf.progress.percent == 1.0

    @pytest.mark.asyncio
    async def test_get_run_not_found(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test that a 404 from the API surfaces as APIError."""
        from pysourcecraft.models import APIError

        mock_router.get(f"{RUNS_URL}/999").mock(
            return_value=Response(
                404,
                json=create_error_response("not_found", "run not found", 404),
            )
        )

        with pytest.raises(APIError):
            await client.cicd.get_run("testuser", "test-repo", "999")

    @pytest.mark.asyncio
    async def test_run_workflows(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_run_data: dict[str, Any],
    ) -> None:
        """Test triggering workflows posts a RunWorkflowsBody to /cicd/runs."""
        mock_run_data["status"] = "created"
        route = mock_router.post(RUNS_URL).mock(
            return_value=Response(200, json=mock_run_data)
        )

        request = RunWorkflowsRequest(
            head=GitRevision(branch="main"),
            config_revision=GitRevision(commit="abc123"),
            workflows=[
                WorkflowData(
                    name="ci",
                    values=[InputValue(name="env", value="staging")],
                )
            ],
            shared=False,
        )
        run = await client.cicd.run_workflows("testuser", "test-repo", request)

        assert route.called
        body = route.calls.last.request.read().decode()
        assert '"head":{"branch":"main"}' in body
        assert '"config_revision":{"commit":"abc123"}' in body
        assert '"workflows":[{"name":"ci"' in body
        assert '"shared":false' in body
        assert isinstance(run, Run)
        assert run.status == RunStatus.CREATED

    @pytest.mark.asyncio
    async def test_run_workflows_empty_request(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_run_data: dict[str, Any],
    ) -> None:
        """Test that defaults (empty body) run the default branch."""
        route = mock_router.post(RUNS_URL).mock(
            return_value=Response(200, json=mock_run_data)
        )

        await client.cicd.run_workflows("testuser", "test-repo", RunWorkflowsRequest())

        body = route.calls.last.request.read().decode()
        assert body == '{"workflows":[]}'


class TestCICDClientWorkflow:
    """Tests for workflow retrieval inside a run."""

    @pytest.mark.asyncio
    async def test_get_workflow(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_run_data: dict[str, Any],
    ) -> None:
        """Test getting a workflow launch of a run."""
        wf = mock_run_data["workflows"][0]
        route = mock_router.get(f"{RUNS_URL}/12/ci").mock(
            return_value=Response(200, json=wf)
        )

        result = await client.cicd.get_workflow("testuser", "test-repo", "12", "ci")

        assert route.called
        assert isinstance(result, CIWorkflow)
        assert result.slug == "ci"
        assert result.tasks[0].slug == "build"

    @pytest.mark.asyncio
    async def test_get_workflow_with_current_cube_progress(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test progress carries the cube currently being executed."""
        wf = {
            "id": "",
            "slug": "ci",
            "status": "processing",
            "progress": {
                "percent": 0.5,
                "current_cube": {"slug": "test", "status": "processing"},
            },
        }
        mock_router.get(f"{RUNS_URL}/12/ci").mock(return_value=Response(200, json=wf))

        result = await client.cicd.get_workflow("testuser", "test-repo", "12", "ci")

        assert result.progress is not None
        assert result.progress.percent == 0.5
        assert result.progress.current_cube is not None
        assert result.progress.current_cube.slug == "test"


class TestCICDClientLogs:
    """Tests for cube logs."""

    @pytest.mark.asyncio
    async def test_get_cube_logs(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_logs_data: dict[str, Any],
    ) -> None:
        """Test fetching cube logs posts nothing and passes page param."""
        route = mock_router.get(
            f"{BASE}/repos/testuser/test-repo/cicd/logs/12/ci/build/package"
        ).mock(return_value=Response(200, json=mock_logs_data))

        logs = await client.cicd.get_cube_logs(
            "testuser", "test-repo", "12", "ci", "build", "package"
        )

        assert route.called
        assert "page=1" in str(route.calls.last.request.url)
        assert isinstance(logs, GetCubeLogsResponse)
        assert logs.logs == "[2024-01-15] build started"
        assert logs.page_complete
        assert logs.done

    @pytest.mark.asyncio
    async def test_get_cube_logs_pagination(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test subsequent log pages request the given page number."""
        route = mock_router.get(
            f"{BASE}/repos/testuser/test-repo/cicd/logs/12/ci/build/package"
        ).mock(
            return_value=Response(
                200, json={"logs": "more", "page_complete": False, "done": False}
            )
        )

        logs = await client.cicd.get_cube_logs(
            "testuser", "test-repo", "12", "ci", "build", "package", page=3
        )

        assert "page=3" in str(route.calls.last.request.url)
        assert not logs.page_complete
        assert not logs.done


class TestCICDClientArtifacts:
    """Tests for cube artifacts."""

    @pytest.mark.asyncio
    async def test_get_artifacts(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
        mock_cube_artifacts_data: dict[str, Any],
    ) -> None:
        """Test fetching cube artifacts with temporary download URLs."""
        route = mock_router.get(
            f"{BASE}/repos/testuser/test-repo/cicd/artifacts/12/ci/build/package"
        ).mock(return_value=Response(200, json=mock_cube_artifacts_data))

        result = await client.cicd.get_artifacts(
            "testuser", "test-repo", "12", "ci", "build", "package"
        )

        assert route.called
        assert isinstance(result, GetCubeArtifactsResponse)
        assert len(result.artifacts) == 1
        artifact = result.artifacts[0]
        assert artifact.local_path == "dist/app.whl"
        assert artifact.status == "success"
        assert artifact.download_url == "https://sourcecraft.dev/dl/app.whl"

    @pytest.mark.asyncio
    async def test_get_artifacts_empty(
        self,
        client: SourceCraftClient,
        mock_router: respx.MockRouter,
    ) -> None:
        """Test a cube without artifacts yields an empty list."""
        mock_router.get(
            f"{BASE}/repos/testuser/test-repo/cicd/artifacts/12/ci/build/package"
        ).mock(return_value=Response(200, json={"artifacts": []}))

        result = await client.cicd.get_artifacts(
            "testuser", "test-repo", "12", "ci", "build", "package"
        )

        assert result.artifacts == []
