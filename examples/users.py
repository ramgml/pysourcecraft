"""
Users and Organizations API usage examples.
"""

import asyncio
import os

from pysourcecraft import SourceCraftClient, APIError


async def get_current_user():
    """Example: Get the authenticated user."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            user = await client.users.get_current()
            print(f"Current user: {user.username}")
            print(f"Name: {user.name}")
            print(f"Email: {user.email}")
            print(f"Bio: {user.bio}")
            print(f"Location: {user.location}")
            print(f"Public repos: {user.public_repos_count}")
            print(f"Followers: {user.followers_count}")
            print(f"Following: {user.following_count}")
            if user.plan:
                print(f"Plan: {user.plan.name} (Private repos: {user.plan.private_repos})")
            
        except APIError as e:
            print(f"Error getting current user: {e}")


async def get_user_by_username():
    """Example: Get a user by username."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            username = "example-user"  # Replace with actual username
            
            user = await client.users.get(username)
            print(f"User: {user.username}")
            print(f"Name: {user.name}")
            print(f"Bio: {user.bio}")
            print(f"Company: {user.company}")
            print(f"Location: {user.location}")
            print(f"Public repos: {user.public_repos_count}")
            print(f"Followers: {user.followers_count}")
            print(f"Following: {user.following_count}")
            
        except APIError as e:
            if e.status_code == 404:
                print("User not found")
            else:
                print(f"Error getting user: {e}")


async def update_current_user():
    """Example: Update the authenticated user."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # Update user fields (uncomment to test)
            # updated_user = await client.users.update(
            #     name="Updated Name",
            #     bio="Updated bio from PySourceCraft API",
            #     location="New Location"
            # )
            # print(f"✓ Updated user: {updated_user.username}")
            print("Note: Uncomment update code to actually modify user profile")
            
        except APIError as e:
            print(f"Error updating user: {e}")


async def list_user_repositories():
    """Example: List repositories for a user."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # List repositories for current user
            repos = await client.users.list_repos(page=1, per_page=5)
            print(f"Found {repos.total} repositories for current user:")
            for repo in repos.data:
                print(f"  - {repo.full_name} ({repo.visibility.value})")
                print(f"    Description: {repo.description or 'No description'}")
                print()
            
            # List repositories for another user
            username = "example-user"  # Replace with actual username
            other_repos = await client.users.list_repos(username=username, page=1, per_page=3)
            print(f"Found {other_repos.total} repositories for {username}:")
            for repo in other_repos.data:
                print(f"  - {repo.full_name}")
                print(f"    Stars: {repo.stargazers_count}, Forks: {repo.forks_count}")
                print()
                
        except APIError as e:
            if e.status_code == 404:
                print("User not found")
            else:
                print(f"Error listing repositories: {e}")


async def list_user_organizations():
    """Example: List organizations for a user."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            # List organizations for current user
            orgs = await client.users.list_orgs(page=1, per_page=10)
            print(f"Found {orgs.total} organizations for current user:")
            for org in orgs.data:
                print(f"  - {org.login} ({org.name})")
                print(f"    Description: {org.description or 'No description'}")
                print()
            
            # List organizations for another user
            username = "example-user"  # Replace with actual username
            other_orgs = await client.users.list_orgs(username=username, page=1, per_page=5)
            print(f"Found {other_orgs.total} organizations for {username}:")
            for org in other_orgs.data:
                print(f"  - {org.login}")
                print()
                
        except APIError as e:
            if e.status_code == 404:
                print("User not found")
            else:
                print(f"Error listing organizations: {e}")


async def list_organizations():
    """Example: List all organizations."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            orgs = await client.organizations.list(page=1, per_page=5)
            print(f"Found {orgs.total} organizations:")
            for org in orgs.data:
                print(f"  - {org.login} ({org.name})")
                print(f"    Description: {org.description or 'No description'}")
                print(f"    Public repos: {org.public_repos_count}")
                print()
                
        except APIError as e:
            print(f"Error listing organizations: {e}")


async def get_organization_details():
    """Example: Get organization details."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            org_login = "example-org"  # Replace with actual organization login
            
            org = await client.organizations.get(org_login)
            print(f"Organization: {org.login}")
            print(f"Name: {org.name}")
            print(f"Description: {org.description}")
            print(f"Location: {org.location}")
            print(f"Email: {org.email}")
            print(f"Public repos: {org.public_repos_count}")
            print(f"Members: {org.members_count}")
            
        except APIError as e:
            if e.status_code == 404:
                print("Organization not found")
            else:
                print(f"Error getting organization: {e}")


async def list_organization_repositories():
    """Example: List repositories for an organization."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            org_login = "example-org"  # Replace with actual organization login
            
            repos = await client.organizations.list_repos(org_login, page=1, per_page=5)
            print(f"Found {repos.total} repositories for organization {org_login}:")
            for repo in repos.data:
                print(f"  - {repo.full_name} ({repo.visibility.value})")
                print(f"    Description: {repo.description or 'No description'}")
                print(f"    Stars: {repo.stargazers_count}, Forks: {repo.forks_count}")
                print()
                
        except APIError as e:
            if e.status_code == 404:
                print("Organization not found")
            else:
                print(f"Error listing organization repositories: {e}")


async def list_organization_members():
    """Example: List members of an organization."""
    api_token = os.getenv("SOURCECRAFT_API_TOKEN")
    if not api_token:
        print("Please set SOURCECRAFT_API_TOKEN environment variable")
        return
    
    async with SourceCraftClient(api_token=api_token) as client:
        try:
            org_login = "example-org"  # Replace with actual organization login
            
            members = await client.organizations.list_members(org_login, page=1, per_page=10)
            print(f"Found {members.total} members in organization {org_login}:")
            for member in members.data:
                print(f"  - {member.username}")
                print(f"    Name: {member.name}")
                print()
                
        except APIError as e:
            if e.status_code == 404:
                print("Organization not found")
            else:
                print(f"Error listing organization members: {e}")


async def main():
    """Run all users and organizations examples."""
    print("=== Users and Organizations API Examples ===")
    
    await get_current_user()
    print()
    await get_user_by_username()
    print()
    await update_current_user()
    print()
    await list_user_repositories()
    print()
    await list_user_organizations()
    print()
    await list_organizations()
    print()
    await get_organization_details()
    print()
    await list_organization_repositories()
    print()
    await list_organization_members()


if __name__ == "__main__":
    asyncio.run(main())