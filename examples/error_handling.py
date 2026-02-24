"""
Error handling examples for PySourceCraft API client.
"""

import asyncio
import os

from pysourcecraft import SourceCraftClient, APIError


async def basic_error_handling():
    """Example: Basic error handling with try/except."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # This will likely succeed if token is valid
            user = await client.users.get_current()
            print(f"✓ Success: {user.username}")

        except APIError as e:
            print(f"✗ API Error: {e}")
            if e.status_code:
                print(f"  Status Code: {e.status_code}")
            if e.error_response:
                print(f"  Error Type: {e.error_response.error_code}")
                print(f"  Message: {e.error_response.message}")
                if e.error_response.request_id:
                    print(f"  Request ID: {e.error_response.request_id}")
                if e.error_response.details:
                    for key, value in e.error_response.details.items():
                        print(f"  Detail: {key} - {value}")

        except Exception as e:
            print(f"✗ Unexpected error: {e}")


async def handle_specific_http_errors():
    """Example: Handle specific HTTP error codes."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # Try to access a repository that doesn't exist
            owner = "nonexistent-user"
            repo_name = "nonexistent-repo"
            repo = await client.repositories.get(owner, repo_name)
            print(f"Repository: {repo.name}")

        except APIError as e:
            if e.status_code == 401:
                print("✗ Authentication failed: Invalid or missing API token")
            elif e.status_code == 403:
                print("✗ Forbidden: Insufficient permissions for this operation")
            elif e.status_code == 404:
                print("✗ Not Found: Repository or resource does not exist")
            elif e.status_code == 422:
                print("✗ Validation Error: Invalid request data")
                if e.error_response and e.error_response.details:
                    for key, value in e.error_response.details.items():
                        print(f"  - {key}: {value}")
            elif e.status_code and e.status_code >= 500:
                print("✗ Server Error: Temporary server issue, please retry")
            else:
                print(f"✗ API Error: {e}")


async def handle_validation_errors():
    """Example: Handle validation errors when creating resources."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # Try to create a repository with invalid data
            from pysourcecraft.models import CreateRepositoryRequest, RepoVisibility

            create_request = CreateRepositoryRequest(
                name="",  # Invalid: empty name
                description="This should fail due to validation",
                visibility=RepoVisibility.PUBLIC,
            )

            repo = await client.repositories.create(create_request)
            print(f"Created repository: {repo.name}")

        except APIError as e:
            if e.status_code == 422 and e.error_response:
                print("✗ Validation failed:")
                if e.error_response.details:
                    for key, value in e.error_response.details.items():
                        print(f"  - {key}: {value}")
            else:
                print(f"✗ Other error: {e}")


async def handle_network_errors():
    """Example: Handle network-related errors."""
    # Use an invalid base URL to simulate network issues
    async with SourceCraftClient(
        api_token="invalid-token", base_url="https://invalid-url-that-will-fail.com"
    ) as client:
        try:
            user = await client.users.get_current()
            print(f"User: {user.username}")

        except APIError as e:
            if "connection" in str(e).lower() or "timeout" in str(e).lower():
                print("✗ Network error: Unable to connect to the API")
                print(f"  Details: {e}")
            else:
                print(f"✗ API Error: {e}")


async def graceful_error_recovery():
    """Example: Implement graceful error recovery with retries."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return

    async with SourceCraftClient(api_token=api_token) as client:
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                # Simulate an operation that might fail temporarily
                user = await client.users.get_current()
                print(f"✓ Success on attempt {retry_count + 1}: {user.username}")
                break

            except APIError as e:
                if e.status_code and e.status_code >= 500:
                    # Server error - retry
                    retry_count += 1
                    print(f"✗ Server error (attempt {retry_count}): {e}")
                    if retry_count < max_retries:
                        print("  Retrying...")
                        await asyncio.sleep(1)  # Wait before retrying
                    else:
                        print("  Max retries exceeded")
                else:
                    # Client error - don't retry
                    print(f"✗ Client error (not retrying): {e}")
                    break


async def main():
    """Run all error handling examples."""
    print("=== Error Handling Examples ===")

    print("1. Basic error handling:")
    await basic_error_handling()
    print()

    print("2. Specific HTTP error handling:")
    await handle_specific_http_errors()
    print()

    print("3. Validation error handling:")
    await handle_validation_errors()
    print()

    print("4. Network error handling:")
    await handle_network_errors()
    print()

    print("5. Graceful error recovery with retries:")
    await graceful_error_recovery()


if __name__ == "__main__":
    asyncio.run(main())
