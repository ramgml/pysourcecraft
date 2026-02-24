"""
Pull Requests API usage examples.
"""

import asyncio
import os

from pysourcecraft import SourceCraftClient, APIError
from pysourcecraft.models import CreatePullRequestRequest, UpdatePullRequestRequest


async def list_pull_requests():
    """Example: List pull requests in a repository."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # List all pull requests
            prs = await client.pull_requests.list(owner, repo_name, page=1, per_page=5)
            print(f"Found {prs.total} pull requests in {owner}/{repo_name}:")
            for pr in prs.data:
                print(f"  - #{pr.number}: {pr.title}")
                print(f"    State: {pr.state.value}, Author: {pr.user.username}")
                print(f"    Base: {pr.base.ref} <- Head: {pr.head.ref}")
                print(f"    Created: {pr.created_at}")
                print()

        except APIError as e:
            if e.status_code == 404:
                print("Repository not found (make sure to update owner/repo_name)")
            else:
                print(f"Error listing pull requests: {e}")


async def get_pull_request_details():
    """Example: Get specific pull request details."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            pr_number = 1  # Replace with actual PR number

            pr = await client.pull_requests.get(owner, repo_name, pr_number)
            print(f"PR #{pr.number}: {pr.title}")
            print(f"State: {pr.state.value}")
            print(f"Author: {pr.user.username}")
            print(f"Base branch: {pr.base.ref} ({pr.base.sha[:8]})")
            print(f"Head branch: {pr.head.ref} ({pr.head.sha[:8]})")
            print(f"Mergeable: {pr.mergeable}")
            print(f"Created: {pr.created_at}")
            print(f"Updated: {pr.updated_at}")
            print(f"Body: {pr.body[:100] if pr.body else 'No description'}...")

        except APIError as e:
            if e.status_code == 404:
                print("Pull request or repository not found")
            else:
                print(f"Error getting pull request: {e}")


async def create_and_update_pull_request():
    """Example: Create and update a pull request."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # Create pull request
            create_request = CreatePullRequestRequest(
                title="Test PR from PySourceCraft",
                body="This PR was created using the PySourceCraft API client.",
                head="feature-branch",  # Source branch
                base="main",  # Target branch
                draft=False,
            )

            new_pr = await client.pull_requests.create(owner, repo_name, create_request)
            print(f"✓ Created PR #{new_pr.number}: {new_pr.title}")

            # Update pull request
            update_request = UpdatePullRequestRequest(
                title="Updated Test PR from PySourceCraft",
                body="This PR was updated using the PySourceCraft API client.",
            )

            updated_pr = await client.pull_requests.update(
                owner, repo_name, new_pr.number, update_request
            )
            print(f"✓ Updated PR title to: {updated_pr.title}")

        except APIError as e:
            print(f"Error creating/updating pull request: {e}")


async def manage_pull_request_reviews():
    """Example: Add reviews to a pull request."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            pr_number = 1  # Replace with actual PR number

            # Add review comment
            review = await client.pull_requests.create_review(
                owner,
                repo_name,
                pr_number,
                body="This review was added via PySourceCraft API!",
                event="COMMENT",  # Can be "APPROVE", "REQUEST_CHANGES", or "COMMENT"
            )
            print(f"✓ Added review #{review.id} to PR #{pr_number}")

            # List reviews
            reviews = await client.pull_requests.list_reviews(
                owner, repo_name, pr_number
            )
            print(f"Found {reviews.total} reviews on PR #{pr_number}:")
            for review in reviews.data[:2]:  # Show first 2
                print(f"  - {review.user.username}: {review.state.value}")
                print(
                    f"    Comment: {review.body[:50] if review.body else 'No comment'}..."
                )

        except APIError as e:
            if e.status_code == 404:
                print("Pull request or repository not found")
            else:
                print(f"Error managing reviews: {e}")


async def check_pull_request_status():
    """Example: Check status checks on a pull request."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            pr_number = 1  # Replace with actual PR number

            # List status checks
            checks = await client.pull_requests.list_checks(owner, repo_name, pr_number)
            print(f"Found {checks.total} status checks on PR #{pr_number}:")
            for check in checks.data[:3]:  # Show first 3
                print(f"  - {check.name}: {check.state.value}")
                if check.description:
                    print(f"    Description: {check.description}")

        except APIError as e:
            if e.status_code == 404:
                print("Pull request or repository not found")
            else:
                print(f"Error checking status: {e}")


async def main():
    """Run all pull request examples."""
    print("=== Pull Requests API Examples ===")

    await list_pull_requests()
    print()
    await get_pull_request_details()
    print()
    await create_and_update_pull_request()
    print()
    await manage_pull_request_reviews()
    print()
    await check_pull_request_status()


if __name__ == "__main__":
    asyncio.run(main())
