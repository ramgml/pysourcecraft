"""
Comprehensive example showing all PySourceCraft API features.
"""

import asyncio
import os

from pysourcecraft import SourceCraftClient, APIError
from pysourcecraft.models import (
    CreateRepositoryRequest,
    CreateIssueRequest,
    CreatePullRequestRequest,
    CreateReleaseRequest,
    RepoVisibility,
    IssueState
)


# Demonstrate IssueState enum values
print(f"Available issue states: {[state.value for state in IssueState]}")


async def comprehensive_example():
    """Comprehensive example demonstrating multiple API features."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # 1. Get current user
            print("1. Getting current user...")
            user = await client.users.get_current()
            print(f"   Authenticated as: {user.username}")
            
            # 2. Create a test repository
            print("\n2. Creating test repository...")
            repo_request = CreateRepositoryRequest(
                name="pysourcecraft-test-repo",
                description="Test repository created by PySourceCraft examples",
                visibility=RepoVisibility.PRIVATE,
                has_issues=True,
                has_wiki=True
            )
            repo = await client.repositories.create(repo_request)
            print(f"   Created repository: {repo.full_name}")
            
            # 3. Create an issue
            print("\n3. Creating an issue...")
            issue_request = CreateIssueRequest(
                title="Test Issue from Comprehensive Example",
                body="This issue was created as part of the comprehensive PySourceCraft example."
            )
            issue = await client.issues.create(repo.owner.username, repo.name, issue_request)
            print(f"   Created issue #{issue.number}: {issue.title}")
            
            # 4. Create a pull request
            print("\n4. Creating a pull request...")
            pr_request = CreatePullRequestRequest(
                title="Test PR from Comprehensive Example",
                body="This PR was created as part of the comprehensive PySourceCraft example.",
                head="feature-branch",
                base="main",
                draft=False
            )
            # Note: This will likely fail if the branches don't exist, but demonstrates the API call
            try:
                pr = await client.pull_requests.create(repo.owner.username, repo.name, pr_request)
                print(f"   Created PR #{pr.number}: {pr.title}")
            except APIError as e:
                print(f"   Skipped PR creation (expected if branches don't exist): {e}")
            
            # 5. Create a release
            print("\n5. Creating a release...")
            release_request = CreateReleaseRequest(
                tag_name="v1.0.0",
                name="Version 1.0.0",
                body="Initial release created by PySourceCraft examples.",
                draft=False,
                prerelease=False
            )
            release = await client.releases.create(repo.owner.username, repo.name, release_request)
            print(f"   Created release: {release.name} (tag: {release.tag_name})")
            
            # 6. List repositories to verify creation
            print("\n6. Listing repositories...")
            repos = await client.repositories.list(page=1, per_page=5)
            test_repos = [r for r in repos.data if "pysourcecraft-test" in r.name]
            print(f"   Found {len(test_repos)} test repositories")
            
            # 7. Clean up (optional - uncomment to actually delete)
            print("\n7. Cleanup (commented out for safety)...")
            # await client.repositories.delete(repo.owner.username, repo.name)
            # print(f"   Deleted repository: {repo.full_name}")
            
            print("\n✅ Comprehensive example completed successfully!")
            
        except APIError as e:
            print(f"❌ API Error during comprehensive example: {e}")
            if e.status_code:
                print(f"   Status Code: {e.status_code}")
            if e.error_response:
                print(f"   Error Details: {e.error_response.message}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


async def main():
    """Run the comprehensive example."""
    print("=== Comprehensive PySourceCraft API Example ===")
    print("This example demonstrates multiple API features in sequence.")
    print("Note: Some operations may fail if required resources don't exist.")
    print()
    
    await comprehensive_example()


if __name__ == "__main__":
    asyncio.run(main())