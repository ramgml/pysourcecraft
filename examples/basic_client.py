"""
Basic client initialization and usage examples.
"""

import asyncio
import os

from dotenv import load_dotenv
from pysourcecraft import SourceCraftClient, APIError

load_dotenv()


async def basic_client_initialization():
    """Example 1: Basic client initialization with API token."""
    # Method 1: Direct token
    client = SourceCraftClient(api_token="your-api-token-here")

    # Method 2: From environment variable
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    client = SourceCraftClient(api_token=api_token)

    # Method 3: With custom base URL and timeout
    client = SourceCraftClient(
        api_token="your-api-token",
        base_url="https://api.sourcecraft.dev/v1",
        timeout=60.0,
    )

    return client


async def context_manager_usage():
    """Example 2: Using client as async context manager."""
    async with SourceCraftClient(api_token="your-api-token") as client:
        # Client automatically closes when exiting context
        try:
            user = await client.users.get_current()
            print(f"Authenticated as: {user.username}")
        except APIError as e:
            print(f"Note: API call failed as expected with invalid token: {e.message}")


async def main():
    """Run all basic examples."""
    print("=== Basic Client Examples ===")

    # Basic initialization
    client = await basic_client_initialization()
    print(f"✓ Client initialized successfully (base_url: {client.base_url})")

    # Context manager usage
    await context_manager_usage()
    print("✓ Context manager example completed")


if __name__ == "__main__":
    asyncio.run(main())
