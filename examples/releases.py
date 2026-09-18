"""
Releases API usage examples.
"""

import asyncio
import os

from dotenv import load_dotenv
from pysourcecraft import SourceCraftClient, APIError
from pysourcecraft.models import CreateReleaseRequest, UpdateReleaseRequest

load_dotenv()


async def list_releases():
    """Example: List releases in a repository."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # List releases
            releases = await client.releases.list(owner, repo_name, page=1, per_page=5)
            print(f"Found {releases.total} releases in {owner}/{repo_name}:")
            for release in releases.data:
                print(f"  - {release.name or 'Unnamed'} (v{release.tag_name})")
                print(f"    Draft: {release.draft}, Prerelease: {release.prerelease}")
                print(f"    Created: {release.created_at}")
                print(f"    Published: {release.published_at}")
                print()

        except APIError as e:
            if e.status_code == 404:
                print("Repository not found (make sure to update owner/repo_name)")
            else:
                print(f"Error listing releases: {e}")


async def get_release_details():
    """Example: Get specific release details."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            release_id = "12345"  # Replace with actual release ID

            release = await client.releases.get(owner, repo_name, release_id)
            print(f"Release: {release.name or 'Unnamed'}")
            print(f"Tag: {release.tag_name}")
            print(f"Draft: {release.draft}")
            print(f"Prerelease: {release.prerelease}")
            print(f"Author: {release.author.slug if release.author else 'Unknown'}")
            print(f"Created: {release.created_at}")
            print(f"Published: {release.published_at}")
            print(
                f"Body: {release.body[:100] if release.body else 'No description'}..."
            )

        except APIError as e:
            if e.status_code == 404:
                print("Release or repository not found")
            else:
                print(f"Error getting release: {e}")


async def get_release_by_tag():
    """Example: Get release by tag name."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            tag_name = "v1.0.0"  # Replace with actual tag name

            release = await client.releases.get_by_tag(owner, repo_name, tag_name)
            print(f"Release for tag {tag_name}: {release.name or 'Unnamed'}")
            print(f"ID: {release.id}")
            print(f"Published: {release.published_at}")

        except APIError as e:
            if e.status_code == 404:
                print("Release or repository not found")
            else:
                print(f"Error getting release by tag: {e}")


async def get_latest_release():
    """Example: Get the latest release."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            release = await client.releases.get_latest(owner, repo_name)
            print(f"Latest release: {release.name or 'Unnamed'}")
            print(f"Tag: {release.tag_name}")
            print(f"Published: {release.published_at}")

        except APIError as e:
            if e.status_code == 404:
                print("No releases found or repository not found")
            else:
                print(f"Error getting latest release: {e}")


async def create_and_update_release():
    """Example: Create and update a release."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"

            # Create release
            create_request = CreateReleaseRequest(
                tag_name="v1.0.0-test",
                name="Test Release from PySourceCraft",
                body="This release was created using the PySourceCraft API client.",
                publish=False,
            )

            new_release = await client.releases.create(owner, repo_name, create_request)
            print(
                f"✓ Created release: {new_release.name or 'Unnamed'} (ID: {new_release.id})"
            )

            # Update release
            update_request = UpdateReleaseRequest(
                name="Updated Test Release from PySourceCraft",
                body="This release was updated using the PySourceCraft API client.",
            )

            updated_release = await client.releases.update(
                owner, repo_name, new_release.id, update_request
            )
            print(f"✓ Updated release name to: {updated_release.name}")

            # Clean up (optional - be careful with this in production!)
            # await client.releases.delete(owner, repo_name, new_release.id)
            # print("✓ Deleted release")

        except APIError as e:
            print(f"Error creating/updating release: {e}")


async def manage_release_assets():
    """Example: List and upload release assets."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            owner = "your-username"
            repo_name = "your-repo-name"
            release_id = "12345"  # Replace with actual release ID

            # List assets
            assets = await client.releases.list_assets(
                owner, repo_name, release_id, page=1, per_page=5
            )
            print(f"Found {assets.total} assets for release {release_id}:")
            for asset in assets.data:
                print(f"  - {asset.name}")
                if asset.link:
                    print(f"    Download URL: {asset.link}")
                if asset.attachment:
                    print(f"    Size: {asset.attachment.size}")
                    print(f"    MIME Type: {asset.attachment.mime_type}")
                print()

            # Upload asset (uncomment to test with actual file content)
            # sample_content = b"Hello, World!"  # Replace with actual file content
            # uploaded_asset = await client.releases.upload_asset(
            #     owner, repo_name, release_id,
            #     name="test-file.txt",
            #     content=sample_content,
            #     content_type="text/plain"
            # )
            # print(f"✓ Uploaded asset: {uploaded_asset.name} (ID: {uploaded_asset.id})")

        except APIError as e:
            if e.status_code == 404:
                print("Release or repository not found")
            else:
                print(f"Error managing release assets: {e}")


async def main():
    """Run all releases examples."""
    print("=== Releases API Examples ===")

    await list_releases()
    print()
    await get_release_details()
    print()
    await get_release_by_tag()
    print()
    await get_latest_release()
    print()
    await create_and_update_release()
    print()
    await manage_release_assets()


if __name__ == "__main__":
    asyncio.run(main())
