# PySourceCraft

PySourceCraft is an asynchronous Python client library for the SourceCraft API. It provides a clean, type-safe interface to interact with SourceCraft's repositories, issues, pull requests, CI/CD pipelines, releases, users, and organizations.

## Installation

Install PySourceCraft using pip:

```bash
pip install pysourcecraft
```

Or if you're using uv:

```bash
uv pip install pysourcecraft
```

## Basic Usage

The main entry point is the `SourceCraftClient` class, which provides access to all API resources through dedicated client objects.

```python
import asyncio
from pysourcecraft import SourceCraftClient

async def main():
    # Initialize the client with your API token
    async with SourceCraftClient(api_token="your-api-token") as client:
        # Get current user
        user = await client.users.get_current()
        print(f"Hello, {user.username}!")

        # List repositories
        repos = await client.repositories.list()
        for repo in repos.data:
            print(f"- {repo.name}")

# Run the async function
asyncio.run(main())
```

## Authentication

PySourceCraft supports authentication via API tokens. You can provide your token in several ways:

### 1. Direct Token (Recommended)

```python
client = SourceCraftClient(api_token="your-api-token-here")
```

### 2. Environment Variable

Set the `SOURCECRAFT_API_TOKEN` environment variable:

```bash
export SOURCECRAFT_API_TOKEN="your-api-token-here"
```

Then initialize without specifying the token:

```python
client = SourceCraftClient()  # Will read from environment
```

### 3. Configuration File

You can also load the token from a configuration file or any other source:

```python
import os
token = os.getenv("MY_CUSTOM_TOKEN_VAR")
client = SourceCraftClient(api_token=token)
```

**Note**: The API token should have appropriate permissions for the operations you intend to perform.

## Error Handling

PySourceCraft uses a custom `APIError` exception for all API-related errors. This exception provides detailed information about what went wrong.

### Basic Error Handling

```python
from pysourcecraft import SourceCraftClient, APIError

async def safe_api_call():
    try:
        async with SourceCraftClient(api_token="your-token") as client:
            repo = await client.repositories.get("owner", "repo-name")
            return repo
    except APIError as e:
        print(f"API Error: {e}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
        if e.error_response:
            print(f"Error Details: {e.error_response.message}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Common Error Scenarios

- **401 Unauthorized**: Invalid or missing API token
- **403 Forbidden**: Insufficient permissions for the requested operation
- **404 Not Found**: Resource (repository, issue, etc.) doesn't exist
- **422 Unprocessable Entity**: Validation errors in request data
- **5xx Server Errors**: Temporary server issues

The `APIError` exception includes:

- `message`: Human-readable error message
- `status_code`: HTTP status code (if available)
- `error_response`: Full `ErrorResponse` object with detailed error information

## Client Methods Reference

### Main Client (`SourceCraftClient`)

The main client provides access to all resource-specific clients and handles HTTP communication.

**Constructor Parameters:**

- `api_token` (str, optional): API token for authentication
- `base_url` (str): Base URL for the API (default: "<https://api.sourcecraft.dev/v1>")
- `timeout` (float): Request timeout in seconds (default: 30.0)

**HTTP Methods:**

- `get(path, **kwargs)`: Make GET request
- `post(path, **kwargs)`: Make POST request
- `put(path, **kwargs)`: Make PUT request
- `patch(path, **kwargs)`: Make PATCH request
- `delete(path, **kwargs)`: Make DELETE request

### Repositories Client (`client.repositories`)

Manage repositories and their contents.

**Methods:**

- `list(username=None, page=1, per_page=30)`: List repositories for a user
- `list_org_repos(org, page=1, per_page=30)`: List organization repositories
- `get(owner, repo)`: Get repository details
- `create(request)`: Create repository for authenticated user
- `create_org_repo(org, request)`: Create repository in organization
- `update(owner, repo, request)`: Update repository settings
- `delete(owner, repo)`: Delete repository
- `list_branches(owner, repo, page=1, per_page=30)`: List repository branches
- `get_branch(owner, repo, branch)`: Get branch details
- `list_tags(owner, repo, page=1, per_page=30)`: List repository tags

### Issues Client (`client.issues`)

Manage issues and their lifecycle.

**Methods:**

- `list(owner, repo, filters=None, page=1, per_page=30)`: List issues
- `get(owner, repo, issue_number)`: Get issue details
- `create(owner, repo, request)`: Create new issue
- `update(owner, repo, issue_number, request)`: Update issue
- `close(owner, repo, issue_number)`: Close issue
- `reopen(owner, repo, issue_number)`: Reopen issue
- `list_comments(owner, repo, issue_number, page=1, per_page=30)`: List issue comments
- `create_comment(owner, repo, issue_number, body)`: Add comment to issue
- `list_events(owner, repo, issue_number, page=1, per_page=30)`: List issue events

### Pull Requests Client (`client.pull_requests`)

Manage pull requests and code reviews.

**Methods:**

- `list(owner, repo, filters=None, page=1, per_page=30)`: List pull requests
- `get(owner, repo, pull_number)`: Get pull request details
- `create(owner, repo, request)`: Create new pull request
- `update(owner, repo, pull_number, request)`: Update pull request
- `merge(owner, repo, pull_number, request=None)`: Merge pull request
- `list_reviews(owner, repo, pull_number, page=1, per_page=30)`: List PR reviews
- `create_review(owner, repo, pull_number, body=None, event=None)`: Create PR review
- `list_checks(owner, repo, pull_number, page=1, per_page=30)`: List status checks

### CI/CD Client (`client.cicd`)

Inspect and trigger CI/CD runs (token-paginated).

**Runs:**

- `list_runs(owner, repo, page_size=30, page_token=None)`: List CI/CD runs (`RunList`)
- `get_run(owner, repo, run_slug)`: Get run details with workflows/tasks/cubes
- `run_workflows(owner, repo, request)`: Run workflows (`RunWorkflowsRequest`)
- `get_workflow(owner, repo, run_slug, workflow_slug)`: Get a workflow launch in a run

**Logs:**

- `get_cube_logs(owner, repo, run_slug, workflow_slug, task_slug, cube_slug, page=1)`: Get cube logs

**Artifacts:**

- `get_artifacts(owner, repo, run_slug, workflow_slug, task_slug, cube_slug)`: Get cube artifacts (temporary download URLs)

### Releases Client (`client.releases`)

Manage releases and release assets.

**Methods:**

- `list(owner, repo, page=1, per_page=30)`: List releases
- `get(owner, repo, release_id)`: Get release by ID
- `get_by_tag(owner, repo, tag)`: Get release by tag
- `get_latest(owner, repo)`: Get latest release
- `create(owner, repo, request)`: Create new release
- `update(owner, repo, release_id, request)`: Update release
- `delete(owner, repo, release_id)`: Delete release
- `list_assets(owner, repo, release_id, page=1, per_page=30)`: List release assets
- `upload_asset(owner, repo, release_id, name, content, content_type="application/octet-stream")`: Upload asset
- `delete_asset(owner, repo, asset_id)`: Delete release asset

### Users Client (`client.users`)

Manage user accounts and personal repositories.

**Methods:**

- `get_current()`: Get authenticated user
- `get(username)`: Get user by username
- `update(**kwargs)`: Update authenticated user
- `list_repos(username=None, page=1, per_page=30)`: List user repositories
- `list_orgs(username=None, page=1, per_page=30)`: List user organizations

### Organizations Client (`client.organizations`)

Manage organizations and their members.

**Methods:**

- `list(page=1, per_page=30)`: List organizations
- `get(org)`: Get organization details
- `update(org, **kwargs)`: Update organization
- `list_repos(org, page=1, per_page=30)`: List organization repositories
- `list_members(org, page=1, per_page=30)`: List organization members
- `get_membership(org, username)`: Get user membership
- `update_membership(org, username, role)`: Update user membership role
- `remove_member(org, username)`: Remove member from organization

## Pagination

All list methods support pagination and return `PaginatedResponse[T]` objects with the following properties:

- `data`: List of items
- `total`: Total number of items
- `page`: Current page number
- `per_page`: Items per page
- `total_pages`: Total number of pages
- `has_next`: Boolean indicating if there's a next page
- `has_prev`: Boolean indicating if there's a previous page

Example pagination handling:

```python
async def get_all_repos(client):
    all_repos = []
    page = 1

    while True:
        response = await client.repositories.list(page=page, per_page=100)
        all_repos.extend(response.data)

        if not response.has_next:
            break
        page += 1

    return all_repos
```

## Context Manager Support

The `SourceCraftClient` supports async context managers for automatic resource cleanup:

```python
async with SourceCraftClient(api_token="your-token") as client:
    # Use the client
    user = await client.users.get_current()
    # Client automatically closes when exiting the context
```

## Requirements

- Python 3.8+
- httpx >= 0.23.0
- pydantic >= 2.0.0

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.
