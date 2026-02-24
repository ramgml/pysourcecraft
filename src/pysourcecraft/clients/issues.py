"""Issues API client."""

from __future__ import annotations

from pysourcecraft.clients.base import BaseResourceClient
from pysourcecraft.models import (
    CreateIssueRequest,
    Issue,
    IssueComment,
    IssueEvent,
    IssueFilters,
    PaginatedResponse,
    UpdateIssueRequest,
)


class IssuesClient(BaseResourceClient):
    """Client for Issues API."""

    async def list(
        self,
        owner: str,
        repo: str,
        filters: IssueFilters | None = None,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[Issue]:
        """List issues in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            filters: Optional filters
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of issues
        """
        params = self._paginated_params(page=page, per_page=per_page)
        if filters:
            params.update(filters.model_dump(exclude_none=True))

        data = await self._get(f"/repos/{owner}/{repo}/issues", params=params)
        return PaginatedResponse[Issue].model_validate(data)

    async def get(self, owner: str, repo: str, issue_number: int) -> Issue:
        """Get a single issue.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number

        Returns:
            Issue details
        """
        data = await self._get(f"/repos/{owner}/{repo}/issues/{issue_number}")
        return Issue.model_validate(data)

    async def create(self, owner: str, repo: str, request: CreateIssueRequest) -> Issue:
        """Create a new issue.

        Args:
            owner: Repository owner
            repo: Repository name
            request: Issue creation request

        Returns:
            Created issue
        """
        data = await self._post(
            f"/repos/{owner}/{repo}/issues",
            json=request.model_dump(exclude_none=True),
        )
        return Issue.model_validate(data)

    async def update(
        self, owner: str, repo: str, issue_number: int, request: UpdateIssueRequest
    ) -> Issue:
        """Update an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number
            request: Issue update request

        Returns:
            Updated issue
        """
        data = await self._patch(
            f"/repos/{owner}/{repo}/issues/{issue_number}",
            json=request.model_dump(exclude_none=True),
        )
        return Issue.model_validate(data)

    async def close(self, owner: str, repo: str, issue_number: int) -> Issue:
        """Close an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number

        Returns:
            Closed issue
        """
        from pysourcecraft.models import IssueState

        return await self.update(
            owner, repo, issue_number, UpdateIssueRequest(state=IssueState.CLOSED)
        )

    async def reopen(self, owner: str, repo: str, issue_number: int) -> Issue:
        """Reopen an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number

        Returns:
            Reopened issue
        """
        from pysourcecraft.models import IssueState

        return await self.update(
            owner, repo, issue_number, UpdateIssueRequest(state=IssueState.OPEN)
        )

    async def list_comments(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[IssueComment]:
        """List comments on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of comments
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(
            f"/repos/{owner}/{repo}/issues/{issue_number}/comments", params=params
        )
        return PaginatedResponse[IssueComment].model_validate(data)

    async def create_comment(
        self, owner: str, repo: str, issue_number: int, body: str
    ) -> IssueComment:
        """Create a comment on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number
            body: Comment body

        Returns:
            Created comment
        """
        data = await self._post(
            f"/repos/{owner}/{repo}/issues/{issue_number}/comments",
            json={"body": body},
        )
        return IssueComment.model_validate(data)

    async def list_events(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[IssueEvent]:
        """List events for an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of events
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(
            f"/repos/{owner}/{repo}/issues/{issue_number}/events", params=params
        )
        return PaginatedResponse[IssueEvent].model_validate(data)