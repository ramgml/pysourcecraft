"""Repositories API client."""

from __future__ import annotations

from pysourcecraft.clients.base import BaseResourceClient
from pysourcecraft.models import (
    CreateRepositoryRequest,
    ListOrganizationRepositoriesResponse,
    PaginatedResponse,
    RepoBranch,
    RepoTag,
    Repository,
    UpdateRepositoryRequest,
)


class RepositoriesClient(BaseResourceClient):
    """Client for Repositories API."""

    async def list(
        self,
        username: str | None = None,
        page: int = 1,
        per_page: int = 30,
    ) -> ListOrganizationRepositoriesResponse:
        """List repositories.

        Args:
            username: Filter by username (None for authenticated user)
            page: Page number
            per_page: Items per page

        Returns:
            List of repositories with next page token
        """
        params = self._paginated_params(page=page, per_page=per_page)

        if username:
            data = await self._get(f"/users/{username}/repos", params=params)
        else:
            data = await self._get("/repos", params=params)

        return ListOrganizationRepositoriesResponse.model_validate(data)

    async def list_org_repos(
        self,
        org: str,
        page: int = 1,
        per_page: int = 30,
    ) -> ListOrganizationRepositoriesResponse:
        """List organization repositories.

        Args:
            org: Organization name
            page: Page number
            per_page: Items per page

        Returns:
            List of organization repositories with pagination token
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(f"/orgs/{org}/repos", params=params)
        return ListOrganizationRepositoriesResponse.model_validate(data)

    async def get(self, owner: str, repo: str) -> Repository:
        """Get a single repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Repository details
        """
        data = await self._get(f"/repos/{owner}/{repo}")
        return Repository.model_validate(data)

    async def create(self, request: CreateRepositoryRequest) -> Repository:
        """Create a new repository for the authenticated user.

        Args:
            request: Repository creation request

        Returns:
            Created repository
        """
        data = await self._post(
            "/repos",
            json=request.model_dump(exclude_none=True),
        )
        return Repository.model_validate(data)

    async def create_org_repo(
        self, org: str, request: CreateRepositoryRequest
    ) -> Repository:
        """Create a new repository in an organization.

        Args:
            org: Organization name
            request: Repository creation request

        Returns:
            Created repository
        """
        data = await self._post(
            f"/orgs/{org}/repos",
            json=request.model_dump(exclude_none=True),
        )
        return Repository.model_validate(data)

    async def update(
        self, owner: str, repo: str, request: UpdateRepositoryRequest
    ) -> Repository:
        """Update a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            request: Repository update request

        Returns:
            Updated repository
        """
        data = await self._patch(
            f"/repos/{owner}/{repo}",
            json=request.model_dump(exclude_none=True),
        )
        return Repository.model_validate(data)

    async def delete(self, owner: str, repo: str) -> None:
        """Delete a repository.

        Args:
            owner: Repository owner
            repo: Repository name
        """
        await self._delete(f"/repos/{owner}/{repo}")

    async def list_branches(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[RepoBranch]:
        """List branches in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of branches
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(f"/repos/{owner}/{repo}/branches", params=params)
        return PaginatedResponse[RepoBranch].model_validate(data)

    async def get_branch(self, owner: str, repo: str, branch: str) -> RepoBranch:
        """Get a single branch.

        Args:
            owner: Repository owner
            repo: Repository name
            branch: Branch name

        Returns:
            Branch details
        """
        data = await self._get(f"/repos/{owner}/{repo}/branches/{branch}")
        return RepoBranch.model_validate(data)

    async def list_tags(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[RepoTag]:
        """List tags in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of tags
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(f"/repos/{owner}/{repo}/tags", params=params)
        return PaginatedResponse[RepoTag].model_validate(data)
