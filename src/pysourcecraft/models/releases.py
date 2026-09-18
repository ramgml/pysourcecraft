"""Pydantic models for Releases."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import AliasChoices, Field, model_validator

from pysourcecraft.models.base import BaseModel
from pysourcecraft.models.users import UserEmbedded


class ReleaseStatus(str, Enum):
    """Release status enum.

    Matches swagger schema Release.Status definition.
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    DISCARDED = "discarded"


class Attachment(BaseModel):
    """Attachment model.

    Matches swagger schema Attachment definition.
    """

    id: str = Field(description="Attachment ID")
    name: str = Field(description="Attachment name")
    mime_type: str = Field(description="MIME type")
    file_type: str | None = Field(None, description="File type")
    size: str = Field(description="File size")


class ReleaseAsset(BaseModel):
    """Release asset model.

    Matches swagger schema ReleaseAsset definition.
    """

    id: str = Field(description="Asset ID")
    name: str = Field(description="Asset name")
    link: str | None = Field(None, description="Asset link")
    attachment: Attachment | None = Field(None, description="Attachment details")


class Release(BaseModel):
    """Release model.

    Matches swagger schema Release definition.
    """

    id: str = Field(description="Release ID")
    repo_id: str = Field(description="Repository ID")
    author: UserEmbedded | None = Field(None, description="Release author")
    tag: str = Field(description="Release tag (also serves as its slug)")
    hash: str = Field(description="Git hash")
    title: str | None = Field(None, description="Release title")
    release_notes: str | None = Field(None, description="Release notes")
    status: ReleaseStatus = Field(description="Release status")
    assets: list[ReleaseAsset] = Field(
        default_factory=list, description="Release assets"
    )
    is_latest: bool = Field(description="Whether this is the latest release")
    is_pre_release: bool = Field(description="Whether this is a pre-release")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    released_at: datetime | None = Field(None, description="Release timestamp")

    # Backward compatibility property
    @property
    def name(self) -> str | None:
        """Backward compatibility: returns title as name."""
        return self.title

    @property
    def tag_name(self) -> str:
        """Backward compatibility: returns tag as tag_name."""
        return self.tag

    @property
    def body(self) -> str | None:
        """Backward compatibility: returns release_notes as body."""
        return self.release_notes

    @property
    def prerelease(self) -> bool:
        """Backward compatibility: returns is_pre_release as prerelease."""
        return self.is_pre_release

    @property
    def draft(self) -> bool:
        """Backward compatibility: returns if status is draft."""
        return self.status == ReleaseStatus.DRAFT

    @property
    def published_at(self) -> datetime | None:
        """Backward compatibility: returns released_at as published_at."""
        return self.released_at


# Backward compatibility aliases
ReleaseState = ReleaseStatus


class ReleaseAuthor(UserEmbedded):
    """Release author reference (backward compatibility alias).

    .. deprecated:: Use UserEmbedded instead.
    """

    pass


class CreateReleaseRequest(BaseModel):
    """Request to create a release.

    Body per sourcecraft.swagger.json CreateReleaseBody:
    ``{tag, target_branch, title, release_notes, publish}``.
    GitHub-style names (name/body/draft/target_commitish/...) are accepted
    via aliases but are sent in the API shape.
    """

    tag_name: str = Field(
        min_length=1,
        validation_alias=AliasChoices("tag_name", "tag"),
        serialization_alias="tag",
    )
    name: str | None = Field(
        None,
        validation_alias=AliasChoices("name", "title"),
        serialization_alias="title",
        description="Release name",
    )
    body: str | None = Field(
        None,
        validation_alias=AliasChoices("body", "release_notes"),
        serialization_alias="release_notes",
        description="Release notes",
    )
    draft: bool | None = Field(
        None, description="Create as draft (API wants publish=true when not draft)"
    )
    prerelease: bool | None = Field(
        None,
        validation_alias=AliasChoices("prerelease", "pre_release", "is_pre_release"),
        serialization_alias="is_pre_release",
        description="Mark release as a pre-release (API: is_pre_release)",
    )
    publish: bool | None = Field(
        None, description="Publish immediately instead of creating a draft"
    )
    target_commitish: str | None = Field(
        None,
        validation_alias=AliasChoices("target_commitish", "target_branch"),
        serialization_alias="target_branch",
        description="Target commit/branch",
    )

    @model_validator(mode="after")
    def _map_draft_to_publish(self) -> CreateReleaseRequest:
        # GitHub-style `draft=not publish` (used by the CLI) maps to the
        # API's `publish` flag.
        if self.publish is None and self.draft is not None:
            self.publish = not self.draft
        if self.publish is None:
            self.publish = False
        return self


class UpdateReleaseRequest(BaseModel):
    """Request to update a release.

    Body per sourcecraft.swagger.json UpdateReleaseBody:
    ``{title, release_notes}``.
    """

    tag_name: str | None = Field(
        None,
        min_length=1,
        validation_alias=AliasChoices("tag_name", "tag"),
        serialization_alias="tag",
        description="Git tag name",
    )
    name: str | None = Field(
        None,
        validation_alias=AliasChoices("name", "title"),
        serialization_alias="title",
        description="Release name",
    )
    body: str | None = Field(
        None,
        validation_alias=AliasChoices("body", "release_notes"),
        serialization_alias="release_notes",
        description="Release notes",
    )
