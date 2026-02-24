"""CI/CD API client."""

from __future__ import annotations

from pysourcecraft.clients.base import BaseResourceClient
from pysourcecraft.models import (
    Artifact,
    PaginatedResponse,
    Pipeline,
    Workflow,
    WorkflowRun,
)


class CICDClient(BaseResourceClient):
    """Client for CI/CD API."""

    # Workflows
    async def list_workflows(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[Workflow]:
        """List workflows in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of workflows
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(f"/repos/{owner}/{repo}/workflows", params=params)
        return PaginatedResponse[Workflow].model_validate(data)

    async def get_workflow(self, owner: str, repo: str, workflow_id: str) -> Workflow:
        """Get a single workflow.

        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Workflow ID

        Returns:
            Workflow details
        """
        data = await self._get(f"/repos/{owner}/{repo}/workflows/{workflow_id}")
        return Workflow.model_validate(data)

    # Workflow Runs
    async def list_workflow_runs(
        self,
        owner: str,
        repo: str,
        workflow_id: str | None = None,
        branch: str | None = None,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[WorkflowRun]:
        """List workflow runs.

        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Optional workflow ID filter
            branch: Optional branch filter
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of workflow runs
        """
        params = self._paginated_params(page=page, per_page=per_page)
        if branch:
            params["branch"] = branch

        if workflow_id:
            data = await self._get(
                f"/repos/{owner}/{repo}/workflows/{workflow_id}/runs", params=params
            )
        else:
            data = await self._get(f"/repos/{owner}/{repo}/actions/runs", params=params)

        return PaginatedResponse[WorkflowRun].model_validate(data)

    async def get_workflow_run(self, owner: str, repo: str, run_id: str) -> WorkflowRun:
        """Get a single workflow run.

        Args:
            owner: Repository owner
            repo: Repository name
            run_id: Run ID

        Returns:
            Workflow run details
        """
        data = await self._get(f"/repos/{owner}/{repo}/actions/runs/{run_id}")
        return WorkflowRun.model_validate(data)

    async def cancel_workflow_run(self, owner: str, repo: str, run_id: str) -> None:
        """Cancel a workflow run.

        Args:
            owner: Repository owner
            repo: Repository name
            run_id: Run ID
        """
        await self._post(f"/repos/{owner}/{repo}/actions/runs/{run_id}/cancel")

    async def rerun_workflow_run(self, owner: str, repo: str, run_id: str) -> None:
        """Re-run a workflow run.

        Args:
            owner: Repository owner
            repo: Repository name
            run_id: Run ID
        """
        await self._post(f"/repos/{owner}/{repo}/actions/runs/{run_id}/rerun")

    # Pipelines
    async def list_pipelines(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[Pipeline]:
        """List pipelines in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of pipelines
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(f"/repos/{owner}/{repo}/pipelines", params=params)
        return PaginatedResponse[Pipeline].model_validate(data)

    async def get_pipeline(self, owner: str, repo: str, pipeline_id: str) -> Pipeline:
        """Get a single pipeline.

        Args:
            owner: Repository owner
            repo: Repository name
            pipeline_id: Pipeline ID

        Returns:
            Pipeline details
        """
        data = await self._get(f"/repos/{owner}/{repo}/pipelines/{pipeline_id}")
        return Pipeline.model_validate(data)

    async def create_pipeline(
        self, owner: str, repo: str, ref: str, variables: dict | None = None
    ) -> Pipeline:
        """Create a new pipeline.

        Args:
            owner: Repository owner
            repo: Repository name
            ref: Git ref (branch/tag)
            variables: Pipeline variables

        Returns:
            Created pipeline
        """
        json_data = {"ref": ref}
        if variables:
            json_data["variables"] = variables

        data = await self._post(
            f"/repos/{owner}/{repo}/pipelines",
            json=json_data,
        )
        return Pipeline.model_validate(data)

    async def retry_pipeline(self, owner: str, repo: str, pipeline_id: str) -> Pipeline:
        """Retry a failed pipeline.

        Args:
            owner: Repository owner
            repo: Repository name
            pipeline_id: Pipeline ID

        Returns:
            New pipeline
        """
        data = await self._post(f"/repos/{owner}/{repo}/pipelines/{pipeline_id}/retry")
        return Pipeline.model_validate(data)

    async def cancel_pipeline(
        self, owner: str, repo: str, pipeline_id: str
    ) -> Pipeline:
        """Cancel a pipeline.

        Args:
            owner: Repository owner
            repo: Repository name
            pipeline_id: Pipeline ID

        Returns:
            Cancelled pipeline
        """
        data = await self._post(f"/repos/{owner}/{repo}/pipelines/{pipeline_id}/cancel")
        return Pipeline.model_validate(data)

    # Artifacts
    async def list_artifacts(
        self,
        owner: str,
        repo: str,
        run_id: str | None = None,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[Artifact]:
        """List artifacts.

        Args:
            owner: Repository owner
            repo: Repository name
            run_id: Optional workflow run ID filter
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of artifacts
        """
        params = self._paginated_params(page=page, per_page=per_page)

        if run_id:
            data = await self._get(
                f"/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts",
                params=params,
            )
        else:
            data = await self._get(
                f"/repos/{owner}/{repo}/actions/artifacts",
                params=params,
            )

        return PaginatedResponse[Artifact].model_validate(data)

    async def get_artifact(self, owner: str, repo: str, artifact_id: str) -> Artifact:
        """Get a single artifact.

        Args:
            owner: Repository owner
            repo: Repository name
            artifact_id: Artifact ID

        Returns:
            Artifact details
        """
        data = await self._get(f"/repos/{owner}/{repo}/actions/artifacts/{artifact_id}")
        return Artifact.model_validate(data)

    async def delete_artifact(self, owner: str, repo: str, artifact_id: str) -> None:
        """Delete an artifact.

        Args:
            owner: Repository owner
            repo: Repository name
            artifact_id: Artifact ID
        """
        await self._delete(f"/repos/{owner}/{repo}/actions/artifacts/{artifact_id}")

    async def download_artifact(self, owner: str, repo: str, artifact_id: str) -> bytes:
        """Download an artifact.

        Args:
            owner: Repository owner
            repo: Repository name
            artifact_id: Artifact ID

        Returns:
            Artifact content as bytes
        """
        response = await self._client.client.get(
            f"/repos/{owner}/{repo}/actions/artifacts/{artifact_id}/zip"
        )
        response.raise_for_status()
        return response.content
