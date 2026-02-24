"""
Issues API usage examples.
"""

import asyncio
import os

from pysourcecraft import SourceCraftClient, APIError
from pysourcecraft.models import CreateIssueRequest, UpdateIssueRequest


async def list_issues():
    """Example: List issues in a repository."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # List all issues
            issues = await client.issues.list(owner, repo_name, page=1, per_page=5)
            print(f"Found {issues.total} issues in {owner}/{repo_name}:")
            for issue in issues.data:
                print(f"  - {issue.slug}: {issue.title}")
                print(f"    State: {issue.status.name}, Author: {issue.author.slug}")
                print(f"    Created: {issue.created_at}")
                print()

        except APIError as e:
            if e.status_code == 404:
                print("Repository not found (make sure to update owner/repo_name)")
            else:
                print(f"Error listing issues: {e}")


async def get_issue_details():
    """Example: Get specific issue details."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            issue_number = 1  # Replace with actual issue number

            issue = await client.issues.get(owner, repo_name, issue_number)
            print(f"Issue {issue.slug}: {issue.title}")
            print(f"State: {issue.status.name}")
            print(f"Author: {issue.author.slug}")
            assignee = issue.assignee.slug if issue.assignee else "Unassigned"
            print(f"Assignee: {assignee}")
            print(f"Labels: {[label.name for label in issue.labels]}")
            print(f"Created: {issue.created_at}")
            print(f"Updated: {issue.updated_at}")
            print(
                f"Description: {issue.description[:100] if issue.description else 'No description'}..."
            )

        except APIError as e:
            if e.status_code == 404:
                print("Issue or repository not found")
            else:
                print(f"Error getting issue: {e}")


async def create_and_update_issue():
    """Example: Create and update an issue."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            issue_number = 1  # Replace with actual issue number

            # Create issue
            create_request = CreateIssueRequest(
                title="Test Issue from PySourceCraft",
                body="This issue was created using the PySourceCraft API client.",
                # Note: assignee_ids and label_ids require valid user/label IDs
            )

            new_issue = await client.issues.create(owner, repo_name, create_request)
            print(f"✓ Created issue {new_issue.slug}: {new_issue.title}")

            # Update issue
            update_request = UpdateIssueRequest(
                title="Updated Test Issue from PySourceCraft",
                body="This issue was updated using the PySourceCraft API client.",
            )

            updated_issue = await client.issues.update(
                owner, repo_name, issue_number, update_request
            )
            print(f"✓ Updated issue title to: {updated_issue.title}")

            # Close issue
            closed_issue = await client.issues.close(owner, repo_name, issue_number)
            print(f"✓ Closed issue {closed_issue.slug}")

            # Reopen issue
            reopened_issue = await client.issues.reopen(owner, repo_name, issue_number)
            print(f"✓ Reopened issue {reopened_issue.slug}")

        except APIError as e:
            print(f"Error creating/updating issue: {e}")


async def manage_issue_comments():
    """Example: Add comments to an issue."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            issue_number = 1  # Replace with actual issue number

            # Add comment
            comment = await client.issues.create_comment(
                owner,
                repo_name,
                issue_number,
                "This comment was added via PySourceCraft API!",
            )
            print(f"✓ Added comment #{comment.id} to issue #{issue_number}")

            # List comments
            comments = await client.issues.list_comments(owner, repo_name, issue_number)
            print(f"Found {comments.total} comments on issue #{issue_number}:")
            for comment in comments.data[:2]:  # Show first 2
                print(f"  - {comment.author.slug}: {comment.body[:50]}...")

        except APIError as e:
            if e.status_code == 404:
                print("Issue or repository not found")
            else:
                print(f"Error managing comments: {e}")


async def main():
    """Run all issues examples."""
    print("=== Issues API Examples ===")

    await list_issues()
    print()
    await get_issue_details()
    print()
    await create_and_update_issue()
    print()
    await manage_issue_comments()


if __name__ == "__main__":
    asyncio.run(main())
