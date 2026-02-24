"""Pydantic models for Releases."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel


class ReleaseState(str, Enum):
    """Release state enum."""

    PUBLISHED = "published"
    DRAFT = "draft"
    PRERELEASE = "prerelease"


class ReleaseAsset(BaseModel):
    """Release asset model."""

    id: str = Field(description="Asset ID")
    name: str = Field(description="Asset name")
    content_type: str = Field(description="Content type (MIME)")
    size: int = Field(ge=0, description="File size in bytes")
    download_count: int = Field(default=0, ge=0, description="Download count")
    url: str = Field(description="API URL")
    browser_download_url: str = Field(description="Download URL")
    created_at: datetime = Field(description="Upload timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class ReleaseAuthor(BaseModel):
    """Release author reference."""

    id: str = Field(description="User ID")
    username: str = Field(description="Username")
    avatar_url: str | None = Field(None, description="Avatar URL")


class Release(BaseModel):
    """Release model."""

    id: str = Field(description="Release ID")
    tag_name: str = Field(description="Git tag name")
    name: str | None = Field(None, description="Release name")
    body: str | None = Field(None, description="Release notes")
    url: str = Field(description="API URL")
    html_url: str = Field(description="HTML URL")
    tarball_url: str | None = Field(None, description="Source tarball URL")
    zipball_url: str | None = Field(None, description="Source zipball URL")

    # Author
    author: ReleaseAuthor = Field(description="Release author")

    # Target
    target_commitish: str = Field(description="Target commit/branch")

    # State
    draft: bool = Field(default=False, description="Whether this is a draft")
    prerelease: bool = Field(default=False, description="Whether this is a prerelease")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    published_at: datetime | None = Field(None, description="Publication timestamp")

    # Assets
    assets: list[ReleaseAsset] = Field(default_factory=list, description="Release assets")

    # Discussion
    discussion_url: str | None = Field(None, description="Discussion URL")

    # Reactions
    reactions: dict[str, int] = Field(default_factory=dict, description="Reaction counts")


class CreateReleaseRequest(BaseModel):
    """Request to create a release."""

    tag_name: str = Field(min_length=1, description="Git tag name")
    name: str | None = Field(None, description="Release name")
    body: str | None = Field(None, description="Release notes")
    draft: bool = Field(default=False, description="Create as draft")
    prerelease: bool = Field(default=False, description="Mark as prerelease")
    target_commitish: str | None = Field(None, description="Target commit/branch")
    discussion_category_name: str | None = Field(
        None, description="Create discussion in this category"
    )
    generate_release_notes: bool = Field(
        default=False, description="Auto-generate release notes"
    )


class UpdateReleaseRequest(BaseModel):
    """Request to update a release."""

    tag_name: str | None = Field(None, min_length=1, description="Git tag name")
    name: str | None = Field(None, description="Release name")
    body: str | None = Field(None, description="Release notes")
    draft: bool | None = Field(None, description="Draft status")
    prerelease: bool | None = Field(None, description="Prerelease status")
    discussion_category_name: str | None = Field(
        None, description="Create discussion in this category"
    )