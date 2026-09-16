"""Users and Organizations API client."""

from __future__ import annotations

from pysourcecraft.clients.base import BaseResourceClient
from pysourcecraft.models import (
    Issue,
    OrgMembership,
    Organization,
    PaginatedResponse,
    PullRequest,
    Repository,
    User,
)


class UsersClient(BaseResourceClient):
    """Client for Users API."""

    async def get_current(self) -> User:
        """Get the authenticated user.

        Returns:
            Current user details
        """
        data = await self._get("/user")
        return User.model_validate(data)

    async def get(self, username: str) -> User:
        """Get a user by username.

        Args:
            username: Username

        Returns:
            User details
        """
        data = await self._get(f"/users/{username}")
        return User.model_validate(data)

    async def update(self, **kwargs) -> User:
        """Update the authenticated user.

        Args:
            **kwargs: Fields to update

        Returns:
            Updated user
        """
        data = await self._patch("/user", json=kwargs)
        return User.model_validate(data)

    async def list_repos(
        self,
        username: str | None = None,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[Repository]:
        """List repositories for a user.

        Args:
            username: Username (None for authenticated user)
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of repositories
        """
        params = self._paginated_params(page=page, per_page=per_page)

        if username:
            data = await self._get(f"/users/{username}/repos", params=params)
        else:
            data = await self._get("/repos", params=params)

        # API returns {"repositories": [...]} instead of paginated format
        if "repositories" in data:
            repos = [Repository.model_validate(repo) for repo in data["repositories"]]
            return PaginatedResponse[Repository](
                data=repos,
                total=len(repos),
                page=page,
                per_page=per_page,
                total_pages=1,
            )

        return PaginatedResponse[Repository].model_validate(data)

    async def list_orgs(
        self,
        username: str | None = None,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[Organization]:
        """List organizations for a user.

        Args:
            username: Username (None for authenticated user)
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of organizations
        """
        params = self._paginated_params(page=page, per_page=per_page)

        if username:
            data = await self._get(f"/users/{username}/orgs", params=params)
        else:
            data = await self._get("/user/orgs", params=params)

        return PaginatedResponse[Organization].model_validate(data)

    async def list_my_issues(
        self,
        page_size: int = 30,
        page_token: str | None = None,
    ) -> PaginatedResponse[Issue]:
        """List issues assigned to or created by the authenticated user.

        Endpoint: GET /me/issues (page_size/page_token,
        ListIssuesAssignedToAuthenticatedUserResponse: issues,
        next_page_token).
        """
        params = self._paginated_params(
            per_page=page_size, explicit_token=page_token
        )
        data = await self._get("/me/issues", params=params)
        return PaginatedResponse[Issue].model_validate(data)

    async def list_pull_requests(
        self,
        username: str,
        role: str | None = None,
        page_size: int = 30,
        page_token: str | None = None,
    ) -> PaginatedResponse[PullRequest]:
        """List pull requests of a user.

        Endpoint: GET /users/{user_slug}/pulls (role, page_size,
        page_token; ListRepositoryPullRequestsResponse: pull_requests,
        next_page_token).
        """
        params = self._paginated_params(
            per_page=page_size, explicit_token=page_token
        )
        if role:
            params["role"] = role
        data = await self._get(f"/users/{username}/pulls", params=params)
        return PaginatedResponse[PullRequest].model_validate(data)


class OrganizationsClient(BaseResourceClient):
    """Client for Organizations API."""

    async def list(
        self,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[Organization]:
        """List organizations.

        Args:
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of organizations
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get("/organizations", params=params)
        return PaginatedResponse[Organization].model_validate(data)

    async def get(self, org: str) -> Organization:
        """Get an organization.

        Args:
            org: Organization login

        Returns:
            Organization details
        """
        data = await self._get(f"/orgs/{org}")
        return Organization.model_validate(data)

    async def update(self, org: str, **kwargs) -> Organization:
        """Update an organization.

        Args:
            org: Organization login
            **kwargs: Fields to update

        Returns:
            Updated organization
        """
        data = await self._patch(f"/orgs/{org}", json=kwargs)
        return Organization.model_validate(data)

    async def list_repos(
        self,
        org: str,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[Repository]:
        """List repositories for an organization.

        Args:
            org: Organization login
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of repositories
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(f"/orgs/{org}/repos", params=params)
        return PaginatedResponse[Repository].model_validate(data)

    async def list_members(
        self,
        org: str,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[User]:
        """List members of an organization.

        Args:
            org: Organization login
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of members
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(f"/orgs/{org}/members", params=params)
        return PaginatedResponse[User].model_validate(data)

    async def get_membership(self, org: str, username: str) -> OrgMembership:
        """Get membership of a user in an organization.

        Args:
            org: Organization login
            username: Username

        Returns:
            Membership details
        """
        data = await self._get(f"/orgs/{org}/memberships/{username}")
        return OrgMembership.model_validate(data)

    async def update_membership(
        self, org: str, username: str, role: str
    ) -> OrgMembership:
        """Update membership of a user in an organization.

        Args:
            org: Organization login
            username: Username
            role: Member role (admin/member/billing_manager)

        Returns:
            Updated membership
        """
        data = await self._put(
            f"/orgs/{org}/memberships/{username}",
            json={"role": role},
        )
        return OrgMembership.model_validate(data)

    async def remove_member(self, org: str, username: str) -> None:
        """Remove a member from an organization.

        Args:
            org: Organization login
            username: Username
        """
        await self._delete(f"/orgs/{org}/memberships/{username}")

    async def _put(self, path: str, **kwargs):
        """Make PUT request."""
        return await self._client._request("PUT", path, **kwargs)
