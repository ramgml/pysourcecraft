"""Releases API client."""

from __future__ import annotations

from pysourcecraft.clients.base import BaseResourceClient
from pysourcecraft.models import (
    CreateReleaseRequest,
    PaginatedResponse,
    Release,
    ReleaseAsset,
    UpdateReleaseRequest,
)


class ReleasesClient(BaseResourceClient):
    """Client for Releases API."""

    async def list(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[Release]:
        """List releases in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of releases
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(f"/repos/{owner}/{repo}/releases", params=params)
        return PaginatedResponse[Release].model_validate(data)

    async def get(self, owner: str, repo: str, release_id: str) -> Release:
        """Get a single release by ID.

        Args:
            owner: Repository owner
            repo: Repository name
            release_id: Release ID

        Returns:
            Release details
        """
        data = await self._get(f"/repos/{owner}/{repo}/releases/{release_id}")
        return Release.model_validate(data)

    async def get_by_tag(self, owner: str, repo: str, tag: str) -> Release:
        """Get a release by tag.

        Args:
            owner: Repository owner
            repo: Repository name
            tag: Tag name

        Returns:
            Release details
        """
        data = await self._get(f"/repos/{owner}/{repo}/releases/tags/{tag}")
        return Release.model_validate(data)

    async def get_latest(self, owner: str, repo: str) -> Release:
        """Get the latest release.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Latest release details
        """
        data = await self._get(f"/repos/{owner}/{repo}/releases/latest")
        return Release.model_validate(data)

    async def create(
        self, owner: str, repo: str, request: CreateReleaseRequest
    ) -> Release:
        """Create a new release.

        Args:
            owner: Repository owner
            repo: Repository name
            request: Release creation request

        Returns:
            Created release
        """
        data = await self._post(
            f"/repos/{owner}/{repo}/releases",
            json=request.model_dump(exclude_none=True, by_alias=True),
        )
        return Release.model_validate(data)

    async def update(
        self, owner: str, repo: str, release_id: str, request: UpdateReleaseRequest
    ) -> Release:
        """Update a release.

        The API has no id-based PATCH; updates go by tag
        (PATCH /repos/{o}/{r}/releases/tag/{tag}, UpdateReleaseBody
        {title, release_notes}). ``release_id`` is accepted as a tag
        for backward compatibility.

        Args:
            owner: Repository owner
            repo: Repository name
            release_id: Release tag (legacy param name kept)
            request: Release update request

        Returns:
            Updated release
        """
        data = await self._patch(
            f"/repos/{owner}/{repo}/releases/tag/{release_id}",
            json=request.model_dump(exclude_none=True, by_alias=True),
        )
        return Release.model_validate(data)

    async def update_by_tag(
        self, owner: str, repo: str, tag: str, request: UpdateReleaseRequest
    ) -> Release:
        """Update a release by tag (PATCH /releases/tag/{tag})."""
        data = await self._patch(
            f"/repos/{owner}/{repo}/releases/tag/{tag}",
            json=request.model_dump(exclude_none=True, by_alias=True),
        )
        return Release.model_validate(data)

    async def publish_by_tag(self, owner: str, repo: str, tag: str) -> Release:
        """Publish a draft release by tag
        (POST /releases/tag/{tag}/publish)."""
        data = await self._post(
            f"/repos/{owner}/{repo}/releases/tag/{tag}/publish",
            json={},
        )
        return Release.model_validate(data)

    async def delete(self, owner: str, repo: str, release_id: str) -> None:
        """Delete a release.

        Args:
            owner: Repository owner
            repo: Repository name
            release_id: Release ID
        """
        await self._delete(f"/repos/{owner}/{repo}/releases/{release_id}")

    async def list_assets(
        self,
        owner: str,
        repo: str,
        release_id: str,
        page: int = 1,
        per_page: int = 30,
    ) -> PaginatedResponse[ReleaseAsset]:
        """List assets for a release.

        Args:
            owner: Repository owner
            repo: Repository name
            release_id: Release ID
            page: Page number
            per_page: Items per page

        Returns:
            Paginated list of assets
        """
        params = self._paginated_params(page=page, per_page=per_page)
        data = await self._get(
            f"/repos/{owner}/{repo}/releases/{release_id}/assets", params=params
        )
        return PaginatedResponse[ReleaseAsset].model_validate(data)

    async def upload_asset(
        self,
        owner: str,
        repo: str,
        release_id: str,
        name: str,
        content: bytes,
        content_type: str = "application/octet-stream",
    ) -> ReleaseAsset:
        """Upload an asset to a release.

        Args:
            owner: Repository owner
            repo: Repository name
            release_id: Release ID
            name: Asset name
            content: Asset content
            content_type: Content type (MIME)

        Returns:
            Uploaded asset
        """
        data = await self._post(
            f"/repos/{owner}/{repo}/releases/{release_id}/assets",
            params={"name": name},
            content=content,
            headers={"Content-Type": content_type},
        )
        return ReleaseAsset.model_validate(data)

    async def delete_asset(self, owner: str, repo: str, asset_id: str) -> None:
        """Delete a release asset.

        Args:
            owner: Repository owner
            repo: Repository name
            asset_id: Asset ID
        """
        await self._delete(f"/repos/{owner}/{repo}/releases/assets/{asset_id}")
