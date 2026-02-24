"""
Authentication setup examples.
"""

import asyncio
import os

from pysourcecraft import SourceCraftClient, APIError


async def token_authentication():
    """Example: Using API token for authentication."""
    # Get token from environment variable (recommended)
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # Test authentication by getting current user
            user = await client.users.get_current()
            print(f"✓ Successfully authenticated as: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.name}")
        except APIError as e:
            if e.status_code == 401:
                print("✗ Authentication failed: Invalid or missing API token")
            else:
                print(f"✗ API Error: {e}")


async def unauthenticated_usage():
    """Example: Using client without authentication (limited functionality)."""
    async with SourceCraftClient() as client:
        try:
            # This will likely fail with 401 Unauthorized
            user = await client.users.get_current()
            print(f"User: {user.username}")
        except APIError as e:
            if e.status_code == 401:
                print("Expected: Unauthenticated access to user endpoint fails")
            else:
                print(f"Unexpected error: {e}")


async def main():
    """Run all authentication examples."""
    print("=== Authentication Examples ===")

    await token_authentication()
    print()
    await unauthenticated_usage()


if __name__ == "__main__":
    asyncio.run(main())
