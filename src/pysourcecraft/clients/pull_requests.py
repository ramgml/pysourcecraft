"""Pull Requests API client."""

from __future__ import annotations

from pysourcecraft.clients.base import BaseResourceClient
from pysourcecraft.models import (
    CreatePullRequestRequest,
    MergePullRequestRequest,
    PRCheck,
    PRFilters,
    PRMergeMethod,
    PRReview,
    PaginatedResponse,
    PullRequest,
    UpdatePullRequestRequest,
)


class PullRequestsClient(BaseResourceClient):
    """Client for Pull Requests API."""

    async def list(
        self,
        owner: str,
        repo: str,
        filters: PRFilters | None = None,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[PullRequest]:
        """List pull requests in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            filters: Optional filters
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of pull requests
        """
        params = self._paginated_params(page=page, per_page=per_page)
        if filters:
            params.update(filters.model_dump(exclude_none=True))

        data = await self._get(f"/repos/{owner}/{repo}/pulls", params=params)
        return PaginatedResponse[PullRequest].model_validate(data)

    async def get(self, owner: str, repo: str, pull_number: int) -> PullRequest:
        """Get a single pull request.

        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: Pull request number

        Returns:
            Pull request details
        """
        data = await self._get(f"/repos/{owner}/{repo}/pulls/{pull_number}")
        return PullRequest.model_validate(data)

    async def create(
        self, owner: str, repo: str, request: CreatePullRequestRequest
    ) -> PullRequest:
        """Create a new pull request.

        Args:
            owner: Repository owner
            repo: Repository name
            request: Pull request creation request

        Returns:
            Created pull request
        """
        data = await self._post(
            f"/repos/{owner}/{repo}/pulls",
            json=request.model_dump(exclude_none=True),
        )
        return PullRequest.model_validate(data)

    async def update(
        self, owner: str, repo: str, pull_number: int, request: UpdatePullRequestRequest
    ) -> PullRequest:
        """Update a pull request.

        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: Pull request number
            request: Pull request update request

        Returns:
            Updated pull request
        """
        data = await self._patch(
            f"/repos/{owner}/{repo}/pulls/{pull_number}",
            json=request.model_dump(exclude_none=True),
        )
        return PullRequest.model_validate(data)

    async def merge(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        request: MergePullRequestRequest | None = None,
    ) -> dict:
        """Merge a pull request.

        API contract (verified live + swagger MergeParameters):
        POST /repos/{owner}/{repo}/pulls/{n}/merge with
        ``{"squash": bool}`` -> 202 with an operation id. (The old PUT
        with commit_title/commit_message/method returned 405.)

        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: Pull request number
            request: Optional merge request; only its ``method`` is
                mapped (SQUASH -> squash=true)

        Returns:
            Merge operation payload (operation id / status)
        """
        squash = bool(request and request.method == PRMergeMethod.SQUASH)
        return await self._request(
            "POST",
            f"/repos/{owner}/{repo}/pulls/{pull_number}/merge",
            json={"squash": squash},
        )

    async def publish(self, owner: str, repo: str, pull_number: int) -> PullRequest:
        """Publish a draft pull request.

        Endpoint: POST /repos/{owner}/{repo}/pulls/{n}/publish ->
        the updated PullRequest (verified live).
        """
        data = await self._post(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/publish", json={}
        )
        return PullRequest.model_validate(data)

    async def draft(self, owner: str, repo: str, pull_number: int) -> PullRequest:
        """Convert a pull request back to draft.

        Endpoint: POST /repos/{owner}/{repo}/pulls/{n}/draft.
        """
        data = await self._post(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/draft", json={}
        )
        return PullRequest.model_validate(data)

    async def discard(self, owner: str, repo: str, pull_number: int) -> PullRequest:
        """Discard (close) a pull request.

        Endpoint: POST /repos/{owner}/{repo}/pulls/{n}/discard
        (verified live, returns the updated PullRequest).
        """
        data = await self._post(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/discard", json={}
        )
        return PullRequest.model_validate(data)

    async def list_reviews(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[PRReview]:
        """List reviews on a pull request.

        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: Pull request number
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of reviews
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews", params=params
        )
        return PaginatedResponse[PRReview].model_validate(data)

    async def create_review(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        body: str | None = None,
        event: str | None = None,
    ) -> PRReview:
        """Create a review on a pull request.

        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: Pull request number
            body: Review body
            event: Review event (APPROVE/REQUEST_CHANGES/COMMENT)

        Returns:
            Created review
        """
        json_data = {}
        if body:
            json_data["body"] = body
        if event:
            json_data["event"] = event

        data = await self._post(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews",
            json=json_data,
        )
        return PRReview.model_validate(data)

    async def list_checks(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[PRCheck]:
        """List status checks on a pull request.

        Args:
            owner: Repository owner
            repo: Repository name
            pull_number: Pull request number
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of checks
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/checks", params=params
        )
        return PaginatedResponse[PRCheck].model_validate(data)

    async def _put(self, path: str, **kwargs):
        """Make PUT request."""
        return await self._client._request("PUT", path, **kwargs)

    async def _request(self, method: str, path: str, **kwargs):
        """Make HTTP request."""
        return await self._client._request(method, path, **kwargs)
