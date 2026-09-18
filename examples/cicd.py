"""
CI/CD API usage examples.
"""

import asyncio
import os

from dotenv import load_dotenv
from pysourcecraft import SourceCraftClient, APIError
from pysourcecraft.models import GitRevision, RunWorkflowsRequest, WorkflowData

load_dotenv()


async def list_runs():
    """Example: List CI/CD runs in a repository (token pagination)."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            page = await client.cicd.list_runs("testuser", "test-repo")
            for run in page.runs:
                created = run.dates.created_at if run.dates else None
                print(f"Run #{run.slug}: {run.status} ({run.event_type}) at {created}")
            if page.next_page_token:
                page = await client.cicd.list_runs(
                    "testuser", "test-repo", page_token=page.next_page_token
                )
                print(f"Next page: {len(page.runs)} runs")
        except APIError as e:
            print(f"Error listing runs: {e}")


async def get_run_details():
    """Example: Get a run with its workflow launches (tasks, cubes, progress)."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            run = await client.cicd.get_run("testuser", "test-repo", "12")
            print(f"Run #{run.slug}: {run.status}")
            for wf in run.workflows:
                percent = wf.progress.percent if wf.progress else None
                print(f"  workflow {wf.slug}: {wf.status} ({percent})")
            if run.error_messages:
                print("Errors:", "; ".join(run.error_messages))
        except APIError as e:
            print(f"Error getting run: {e}")


async def trigger_workflows():
    """Example: Run workflows on a branch with input parameters."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            run = await client.cicd.run_workflows(
                "testuser",
                "test-repo",
                RunWorkflowsRequest(
                    head=GitRevision(branch="main"),
                    workflows=[WorkflowData(name="ci")],
                ),
            )
            print(f"Triggered run #{run.slug}: {run.status}")
        except APIError as e:
            print(f"Error triggering workflows: {e}")


async def read_cube_logs():
    """Example: Drill down run -> workflow -> cube logs (pages, in order)."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            wf = await client.cicd.get_workflow("testuser", "test-repo", "12", "ci")
            for task in wf.tasks:
                for cube in task.cubes:
                    page = 1
                    while True:
                        logs = await client.cicd.get_cube_logs(
                            "testuser",
                            "test-repo",
                            "12",
                            "ci",
                            task.slug,
                            cube.slug,
                            page=page,
                        )
                        if logs.logs:
                            print(logs.logs)
                        if logs.done or not logs.page_complete:
                            break
                        page += 1
        except APIError as e:
            print(f"Error reading logs: {e}")


async def fetch_artifacts():
    """Example: Get artifacts of a cube with temporary download URLs."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            result = await client.cicd.get_artifacts(
                "testuser", "test-repo", "12", "ci", "build", "package"
            )
            for artifact in result.artifacts:
                print(f"{artifact.local_path}: {artifact.status}")
                print(f"  {artifact.download_url}")
        except APIError as e:
            print(f"Error fetching artifacts: {e}")


async def main():
    """Run all CI/CD examples."""
    await list_runs()
    await get_run_details()
    await trigger_workflows()
    await read_cube_logs()
    await fetch_artifacts()


if __name__ == "__main__":
    asyncio.run(main())
