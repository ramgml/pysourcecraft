"""
Repositories API usage examples.
"""

import asyncio
import os

from dotenv import load_dotenv
from pysourcecraft import SourceCraftClient, APIError
from pysourcecraft.models import (
    CreateRepositoryRequest,
    UpdateRepositoryRequest,
    RepoVisibility,
)

load_dotenv()


async def list_repositories():
    """Example: List repositories for authenticated user."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # List repositories with pagination
            repos = await client.repositories.list(page=1, per_page=10)
            total = len(repos.repositories)
            print(f"Found {total} repositories:")
            for repo in repos.repositories[:5]:  # Show first 5
                print(f"  - {repo.name} ({repo.visibility.value})")
                print(f"    Description: {repo.description or 'No description'}")
                print(f"    Stars: {repo.stargazers_count}, Forks: {repo.forks_count}")
                print()

            # Check if there are more pages
            if repos.next_page_token:
                print("... and more repositories available on next page")

        except APIError as e:
            print(f"Error listing repositories: {e}")


async def get_repository_details():
    """Example: Get specific repository details."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # Replace with actual owner and repo name
            owner = "your-username"
            repo_name = "your-repo-name"

            repo = await client.repositories.get(owner, repo_name)
            print(f"Repository: {repo.full_name}")
            print(f"Description: {repo.description}")
            print(f"Language: {repo.language}")
            print(f"Created: {repo.created_at}")
            print(f"Last updated: {repo.updated_at}")
            print(f"Default branch: {repo.default_branch}")

        except APIError as e:
            if e.status_code == 404:
                print("Repository not found (make sure to update owner/repo_name)")
            else:
                print(f"Error getting repository: {e}")


async def create_and_update_repository():
    """Example: Create and update a repository."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # Create repository
            create_request = CreateRepositoryRequest(
                name="test-repo-from-api",
                description="Repository created via PySourceCraft API",
                visibility=RepoVisibility.PRIVATE,  # Use enum
                homepage="https://example.com",
                has_issues=True,
                has_wiki=True,
                gitignore_template="Python",
            )

            new_repo = await client.repositories.create(create_request)
            print(f"✓ Created repository: {new_repo.full_name}")

            # Update repository
            update_request = UpdateRepositoryRequest(
                description="Updated description via API",
                visibility=RepoVisibility.PUBLIC,  # Use enum
            )

            updated_repo = await client.repositories.update(
                new_repo.owner.username,  # Use username instead of login
                new_repo.name,
                update_request,
            )
            print(
                f"✓ Updated repository visibility to: {updated_repo.visibility.value}"
            )

            # Clean up (optional - be careful with this in production!)
            # await client.repositories.delete(new_repo.owner.username, new_repo.name)
            # print("✓ Deleted repository")

        except APIError as e:
            print(f"Error creating/updating repository: {e}")


async def list_branches_and_tags():
    """Example: List branches and tags for a repository."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # List branches
            branches = await client.repositories.list_branches(owner, repo_name)
            print(f"Branches in {owner}/{repo_name}:")
            for branch in branches.data[:3]:  # Show first 3
                print(f"  - {branch.name} (protected: {branch.protected})")

            # List tags
            tags = await client.repositories.list_tags(owner, repo_name)
            print(f"\nTags in {owner}/{repo_name}:")
            for tag in tags.data[:3]:  # Show first 3
                print(f"  - {tag.name} ({tag.commit_sha[:8]})")

        except APIError as e:
            if e.status_code == 404:
                print("Repository not found (make sure to update owner/repo_name)")
            else:
                print(f"Error listing branches/tags: {e}")


async def main():
    """Run all repository examples."""
    print("=== Repositories API Examples ===")

    await list_repositories()
    print()
    await get_repository_details()
    print()
    await create_and_update_repository()
    print()
    await list_branches_and_tags()


if __name__ == "__main__":
    asyncio.run(main())
