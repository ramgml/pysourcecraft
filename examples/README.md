# PySourceCraft Examples

This directory contains comprehensive examples demonstrating how to use the PySourceCraft API client library.

## Prerequisites

1. Set your SourceCraft API token as an environment variable:
   ```bash
   export SOURCECRAFT_API_TOKEN="your-api-token-here"
   ```

2. Install the PySourceCraft library:
   ```bash
   pip install pysourcecraft
   ```

## Example Files

- **`basic_client.py`**: Basic client initialization and usage patterns
- **`authentication.py`**: Authentication setup and token management
- **`repositories.py`**: Repository management (create, update, delete, list branches/tags)
- **`issues.py`**: Issue management (create, update, close, comments, events)
- **`pull_requests.py`**: Pull request management (create, update, reviews, status checks)
- **`cicd.py`**: CI/CD operations (workflows, pipelines, artifacts, workflow runs)
- **`releases.py`**: Release management (create, update, assets, get by tag)
- **`users.py`**: User and organization management (profile, repositories, memberships)
- **`error_handling.py`**: Comprehensive error handling patterns
- **`comprehensive_example.py`**: End-to-end example showing multiple API features

## Running Examples

Each example can be run independently:

```bash
# Run a specific example
python examples/repositories.py

# Run the comprehensive example
python examples/comprehensive_example.py
```

## Important Notes

- **Replace placeholder values**: Most examples contain placeholder values like `"your-username"` and `"your-repo-name"`. Replace these with actual values from your SourceCraft account.
- **API permissions**: Ensure your API token has the necessary permissions for the operations you want to perform.
- **Rate limits**: Be mindful of API rate limits when running examples repeatedly.
- **Cleanup**: Some examples create resources (repositories, issues, etc.). The cleanup code is often commented out for safety - uncomment it if you want to automatically clean up created resources.

## Error Handling

The examples include comprehensive error handling patterns. Common errors include:
- **401 Unauthorized**: Invalid or missing API token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **422 Unprocessable Entity**: Validation errors in request data

Refer to `error_handling.py` for detailed error handling strategies.

## Getting Help

If you encounter issues with the examples:
1. Check that your API token is valid and has appropriate permissions
2. Verify that the repository/user names you're using exist
3. Review the [main README](../README.md) for additional documentation
4. Check the [PySourceCraft API documentation](https://api.sourcecraft.dev/docs) for endpoint details