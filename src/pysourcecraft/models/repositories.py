"""Pydantic models for Repositories."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel


class RepoVisibility(str, Enum):
    """Repository visibility enum."""

    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"


class RepoPermission(str, Enum):
    """Repository permission enum."""

    NONE = "none"
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    MAINTAIN = "maintain"


class RepoLanguage(BaseModel):
    """Repository language stats."""

    name: str = Field(description="Language name")
    bytes_count: int = Field(ge=0, description="Bytes of code")
    percentage: float = Field(ge=0, le=100, description="Percentage of codebase")


class RepoOwner(BaseModel):
    """Repository owner reference."""

    id: str = Field(description="Owner ID")
    username: str = Field(description="Owner username")
    type: str = Field(description="Owner type (user/organization)")
    avatar_url: str | None = Field(None, description="Avatar URL")
    html_url: str = Field(description="Profile URL")


class RepoLicense(BaseModel):
    """Repository license information."""

    key: str = Field(description="License key")
    name: str = Field(description="License name")
    spdx_id: str | None = Field(None, description="SPDX identifier")
    url: str | None = Field(None, description="License URL")


class Repository(BaseModel):
    """Repository model."""

    id: str = Field(description="Repository ID")
    name: str = Field(description="Repository name")
    full_name: str = Field(description="Full repository name (owner/repo)")
    description: str | None = Field(None, description="Repository description")
    url: str = Field(description="API URL")
    html_url: str = Field(description="HTML URL")
    clone_url: str = Field(description="Git clone URL")
    ssh_url: str | None = Field(None, description="SSH clone URL")

    # Owner
    owner: RepoOwner = Field(description="Repository owner")

    # Visibility
    visibility: RepoVisibility = Field(description="Repository visibility")
    private: bool = Field(description="Whether repository is private")

    # Default branch
    default_branch: str = Field(description="Default branch name")

    # URLs
    homepage: str | None = Field(None, description="Homepage URL")
    wiki_url: str | None = Field(None, description="Wiki URL")
    issues_url: str | None = Field(None, description="Issues URL")
    pulls_url: str | None = Field(None, description="Pull requests URL")

    # Features
    has_issues: bool = Field(default=True, description="Issues enabled")
    has_projects: bool = Field(default=True, description="Projects enabled")
    has_wiki: bool = Field(default=True, description="Wiki enabled")
    has_discussions: bool = Field(default=False, description="Discussions enabled")
    has_pages: bool = Field(default=False, description="GitHub Pages enabled")

    # Settings
    allow_forking: bool = Field(default=True, description="Allow forking")
    allow_squash_merge: bool = Field(default=True, description="Allow squash merge")
    allow_merge_commit: bool = Field(default=True, description="Allow merge commit")
    allow_rebase_merge: bool = Field(default=True, description="Allow rebase merge")
    delete_branch_on_merge: bool = Field(
        default=False, description="Delete branch on merge"
    )
    squash_merge_commit_title: str = Field(
        default="PR_TITLE", description="Squash merge title"
    )
    squash_merge_commit_message: str = Field(
        default="PR_BODY", description="Squash merge message"
    )
    merge_commit_title: str = Field(
        default="PR_TITLE", description="Merge commit title"
    )
    merge_commit_message: str = Field(
        default="PR_BODY", description="Merge commit message"
    )

    # Topics
    topics: list[str] = Field(default_factory=list, description="Repository topics")

    # License
    license: RepoLicense | None = Field(None, description="License information")

    # Language
    language: str | None = Field(None, description="Primary language")
    languages: list[RepoLanguage] = Field(
        default_factory=list, description="Language breakdown"
    )

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    pushed_at: datetime | None = Field(None, description="Last push timestamp")

    # Fork info
    fork: bool = Field(default=False, description="Whether this is a fork")
    parent_id: str | None = Field(None, description="Parent repository ID (if fork)")
    forks_count: int = Field(default=0, ge=0, description="Number of forks")

    # Counts
    stargazers_count: int = Field(default=0, ge=0, description="Number of stars")
    watchers_count: int = Field(default=0, ge=0, description="Number of watchers")
    open_issues_count: int = Field(default=0, ge=0, description="Number of open issues")
    open_pulls_count: int = Field(default=0, ge=0, description="Number of open PRs")

    # Size
    size_kb: int = Field(default=0, ge=0, description="Repository size in KB")

    # Metadata
    archived: bool = Field(default=False, description="Whether repository is archived")
    disabled: bool = Field(default=False, description="Whether repository is disabled")
    is_template: bool = Field(default=False, description="Whether this is a template")

    # Permissions
    permissions: dict[str, bool] = Field(
        default_factory=dict, description="Current user permissions"
    )


class CreateRepositoryRequest(BaseModel):
    """Request to create a repository."""

    name: str = Field(min_length=1, max_length=100, description="Repository name")
    description: str | None = Field(
        None, max_length=350, description="Repository description"
    )
    visibility: RepoVisibility = Field(
        default=RepoVisibility.PRIVATE, description="Visibility"
    )
    homepage: str | None = Field(None, description="Homepage URL")
    has_issues: bool = Field(default=True, description="Enable issues")
    has_projects: bool = Field(default=True, description="Enable projects")
    has_wiki: bool = Field(default=True, description="Enable wiki")
    has_discussions: bool = Field(default=False, description="Enable discussions")
    is_template: bool = Field(default=False, description="Make this a template")
    allow_squash_merge: bool = Field(default=True, description="Allow squash merge")
    allow_merge_commit: bool = Field(default=True, description="Allow merge commit")
    allow_rebase_merge: bool = Field(default=True, description="Allow rebase merge")
    delete_branch_on_merge: bool = Field(
        default=False, description="Delete branch on merge"
    )
    license_key: str | None = Field(None, description="License key")
    gitignore_template: str | None = Field(None, description="Gitignore template")


class UpdateRepositoryRequest(BaseModel):
    """Request to update a repository."""

    name: str | None = Field(
        None, min_length=1, max_length=100, description="Repository name"
    )
    description: str | None = Field(
        None, max_length=350, description="Repository description"
    )
    visibility: RepoVisibility | None = Field(None, description="Visibility")
    homepage: str | None = Field(None, description="Homepage URL")
    has_issues: bool | None = Field(None, description="Enable issues")
    has_projects: bool | None = Field(None, description="Enable projects")
    has_wiki: bool | None = Field(None, description="Enable wiki")
    has_discussions: bool | None = Field(None, description="Enable discussions")
    default_branch: str | None = Field(None, description="Default branch name")
    allow_squash_merge: bool | None = Field(None, description="Allow squash merge")
    allow_merge_commit: bool | None = Field(None, description="Allow merge commit")
    allow_rebase_merge: bool | None = Field(None, description="Allow rebase merge")
    delete_branch_on_merge: bool | None = Field(
        None, description="Delete branch on merge"
    )
    archived: bool | None = Field(None, description="Archive/unarchive repository")


class RepoBranch(BaseModel):
    """Repository branch model."""

    name: str = Field(description="Branch name")
    commit_sha: str = Field(description="Latest commit SHA")
    protected: bool = Field(default=False, description="Whether branch is protected")
    protection_url: str | None = Field(None, description="Protection API URL")


class RepoTag(BaseModel):
    """Repository tag model."""

    name: str = Field(description="Tag name")
    commit_sha: str = Field(description="Commit SHA")
    tarball_url: str | None = Field(None, description="Tarball URL")
    zipball_url: str | None = Field(None, description="Zipball URL")
