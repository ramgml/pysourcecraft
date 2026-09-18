"""CI/CD API client."""

from __future__ import annotations

from pysourcecraft.clients.base import BaseResourceClient
from pysourcecraft.models import (
    CIWorkflow,
    GetCubeArtifactsResponse,
    GetCubeLogsResponse,
    Run,
    RunList,
    RunWorkflowsRequest,
)


class CICDClient(BaseResourceClient):
    """Client for the CI/CD API (sourcecraft.swagger.json: `/cicd/...`)."""

    # Runs
    async def list_runs(
        self,
        owner: str,
        repo: str,
        page_size: int = 30,
        page_token: str | None = None,
    ) -> RunList:
        """List CI/CD runs in a repository.

        Args:
            owner: Repository owner (org/user slug)
            repo: Repository slug
            page_size: Maximum number of runs to return
            page_token: Pagination token from a previous response
        """
        params = self._paginated_params(per_page=page_size, explicit_token=page_token)
        data = await self._get(f"/repos/{owner}/{repo}/cicd/runs", params=params)
        return RunList.model_validate(data)

    async def get_run(self, owner: str, repo: str, run_slug: str) -> Run:
        """Get a single CI/CD run.

        Args:
            owner: Repository owner (org/user slug)
            repo: Repository slug
            run_slug: Run counter serves as a slug
        """
        data = await self._get(f"/repos/{owner}/{repo}/cicd/runs/{run_slug}")
        return Run.model_validate(data)

    async def run_workflows(
        self,
        owner: str,
        repo: str,
        request: RunWorkflowsRequest,
    ) -> Run:
        """Run CI workflows in a repository.

        Args:
            owner: Repository owner (org/user slug)
            repo: Repository slug
            request: Workflows to run with target/config revisions and inputs
        """
        data = await self._post(
            f"/repos/{owner}/{repo}/cicd/runs",
            json=request.model_dump(exclude_none=True, by_alias=True),
        )
        return Run.model_validate(data)

    async def get_workflow(
        self, owner: str, repo: str, run_slug: str, workflow_slug: str
    ) -> CIWorkflow:
        """Get a workflow launch inside a run (tasks, cubes, progress).

        Args:
            owner: Repository owner (org/user slug)
            repo: Repository slug
            run_slug: Run counter serves as a slug
            workflow_slug: Workflow name as defined in the config
        """
        data = await self._get(
            f"/repos/{owner}/{repo}/cicd/runs/{run_slug}/{workflow_slug}"
        )
        return CIWorkflow.model_validate(data)

    # Logs
    async def get_cube_logs(
        self,
        owner: str,
        repo: str,
        run_slug: str,
        workflow_slug: str,
        task_slug: str,
        cube_slug: str,
        page: int = 1,
    ) -> GetCubeLogsResponse:
        """Get logs from a running CI cube.

        Args:
            owner: Repository owner (org/user slug)
            repo: Repository slug
            run_slug: Run counter serves as a slug
            workflow_slug: Workflow name as defined in the config
            task_slug: Task name as defined in the config
            cube_slug: Cube name as defined in the config
            page: Page number (pages are read in order; next pages may 404
                while the current one is still being written)
        """
        data = await self._get(
            f"/repos/{owner}/{repo}/cicd/logs/{run_slug}/{workflow_slug}"
            f"/{task_slug}/{cube_slug}",
            params={"page": page},
        )
        return GetCubeLogsResponse.model_validate(data)

    # Artifacts
    async def get_artifacts(
        self,
        owner: str,
        repo: str,
        run_slug: str,
        workflow_slug: str,
        task_slug: str,
        cube_slug: str,
    ) -> GetCubeArtifactsResponse:
        """Get artifacts produced by a CI cube.

        Args:
            owner: Repository owner (org/user slug)
            repo: Repository slug
            run_slug: Run counter serves as a slug
            workflow_slug: Workflow name as defined in the config
            task_slug: Task name as defined in the config
            cube_slug: Cube name as defined in the config
        """
        data = await self._get(
            f"/repos/{owner}/{repo}/cicd/artifacts/{run_slug}/{workflow_slug}"
            f"/{task_slug}/{cube_slug}"
        )
        return GetCubeArtifactsResponse.model_validate(data)
