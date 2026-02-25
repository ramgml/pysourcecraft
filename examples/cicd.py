"""
CI/CD API usage examples.
"""

import asyncio
import os

from dotenv import load_dotenv
from pysourcecraft import SourceCraftClient, APIError

load_dotenv()


async def list_workflows():
    """Example: List workflows in a repository."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # List workflows
            workflows = await client.cicd.list_workflows(
                owner, repo_name, page=1, per_page=10
            )
            print(f"Found {workflows.total} workflows in {owner}/{repo_name}:")
            for workflow in workflows.data:
                print(f"  - {workflow.name} (ID: {workflow.id})")
                print(f"    Path: {workflow.path}")
                print(f"    State: {workflow.state}")
                print(f"    Created: {workflow.created_at}")
                print()

        except APIError as e:
            if e.status_code == 404:
                print("Repository not found (make sure to update owner/repo_name)")
            else:
                print(f"Error listing workflows: {e}")


async def get_workflow_details():
    """Example: Get specific workflow details."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            workflow_id = "12345"  # Replace with actual workflow ID

            workflow = await client.cicd.get_workflow(owner, repo_name, workflow_id)
            print(f"Workflow: {workflow.name}")
            print(f"Path: {workflow.path}")
            print(f"State: {workflow.state}")
            print(f"Created: {workflow.created_at}")
            print(f"Updated: {workflow.updated_at}")

        except APIError as e:
            if e.status_code == 404:
                print("Workflow or repository not found")
            else:
                print(f"Error getting workflow: {e}")


async def manage_workflow_runs():
    """Example: List and manage workflow runs."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # List all workflow runs
            runs = await client.cicd.list_workflow_runs(
                owner, repo_name, page=1, per_page=5
            )
            print(f"Found {runs.total} workflow runs in {owner}/{repo_name}:")
            for run in runs.data:
                print(f"  - Run #{run.id}: {run.name}")
                print(
                    f"    Status: {run.state.value}, Conclusion: {run.conclusion.value if run.conclusion else 'pending'}"
                )
                print(f"    Branch: {run.head_branch}")
                print(f"    Started: {run.run_started_at}")
                print()

            # If we have a specific run ID, we can get details
            if runs.data:
                run_id = runs.data[0].id
                run_details = await client.cicd.get_workflow_run(
                    owner, repo_name, run_id
                )
                print(f"Detailed info for run #{run_id}:")
                print(f"  Event: {run_details.event.value}")
                print(f"  Duration: {run_details.duration_seconds} seconds")
                print(f"  Jobs URL: {run_details.jobs_url}")

        except APIError as e:
            if e.status_code == 404:
                print("Repository not found")
            else:
                print(f"Error managing workflow runs: {e}")


async def manage_pipelines():
    """Example: List and create pipelines."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # List pipelines
            pipelines = await client.cicd.list_pipelines(
                owner, repo_name, page=1, per_page=5
            )
            print(f"Found {pipelines.total} pipelines in {owner}/{repo_name}:")
            for pipeline in pipelines.data:
                print(f"  - Pipeline #{pipeline.id}: {pipeline.ref}")
                print(f"    Status: {pipeline.status.value}")
                print(f"    Created: {pipeline.created_at}")
                print()

            # Create a new pipeline (uncomment to test)
            # new_pipeline = await client.cicd.create_pipeline(
            #     owner, repo_name, "main",
            #     variables={"ENV": "production"}
            # )
            # print(f"✓ Created pipeline #{new_pipeline.id}")

        except APIError as e:
            if e.status_code == 404:
                print("Repository not found")
            else:
                print(f"Error managing pipelines: {e}")


async def manage_artifacts():
    """Example: List and download artifacts."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # List all artifacts
            artifacts = await client.cicd.list_artifacts(
                owner, repo_name, page=1, per_page=5
            )
            print(f"Found {artifacts.total} artifacts in {owner}/{repo_name}:")
            for artifact in artifacts.data:
                print(f"  - {artifact.name} (ID: {artifact.id})")
                print(f"    Size: {artifact.size_in_bytes} bytes")
                print(f"    Created: {artifact.created_at}")
                print()

            # If we have an artifact ID, we can download it
            if artifacts.data:
                artifact_id = artifacts.data[0].id
                # Download artifact content
                # artifact_content = await client.cicd.download_artifact(owner, repo_name, artifact_id)
                # print(f"✓ Downloaded artifact {artifact_id} ({len(artifact_content)} bytes)")
                print(
                    f"Note: Uncomment download code to actually download artifact {artifact_id}"
                )

        except APIError as e:
            if e.status_code == 404:
                print("Repository not found")
            else:
                print(f"Error managing artifacts: {e}")


async def main():
    """Run all CI/CD examples."""
    print("=== CI/CD API Examples ===")

    await list_workflows()
    print()
    await get_workflow_details()
    print()
    await manage_workflow_runs()
    print()
    await manage_pipelines()
    print()
    await manage_artifacts()


if __name__ == "__main__":
    asyncio.run(main())
