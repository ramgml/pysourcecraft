"""Pydantic models for Users and Organizations."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from pysourcecraft.models.base import BaseModel


class UserType(str, Enum):
    """User type enum."""

    USER = "User"
    ORGANIZATION = "Organization"
    BOT = "Bot"


class Plan(BaseModel):
    """User/Organization plan."""

    name: str = Field(description="Plan name")
    space: int = Field(description="Storage space")
    private_repos: int = Field(description="Private repositories limit")
    collaborators: int = Field(description="Collaborators limit")


class User(BaseModel):
    """User model."""

    id: str = Field(description="User ID")
    username: str = Field(description="Username")
    type: UserType = Field(description="User type")

    # Profile
    name: str | None = Field(None, description="Display name")
    email: str | None = Field(None, description="Public email")
    bio: str | None = Field(None, description="Bio")
    blog: str | None = Field(None, description="Blog URL")
    company: str | None = Field(None, description="Company")
    location: str | None = Field(None, description="Location")
    hireable: bool | None = Field(None, description="Open to hire")

    # URLs
    url: str = Field(description="API URL")
    html_url: str = Field(description="Profile URL")
    avatar_url: str | None = Field(None, description="Avatar URL")
    gravatar_id: str | None = Field(None, description="Gravatar ID")

    # Timestamps
    created_at: datetime = Field(description="Account creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    # Social
    twitter_username: str | None = Field(None, description="Twitter username")
    followers_count: int = Field(default=0, ge=0, description="Followers count")
    following_count: int = Field(default=0, ge=0, description="Following count")

    # Stats
    public_repos_count: int = Field(
        default=0, ge=0, description="Public repositories count"
    )
    public_gists_count: int = Field(default=0, ge=0, description="Public gists count")
    private_gists_count: int = Field(default=0, ge=0, description="Private gists count")

    # Features
    two_factor_authentication: bool | None = Field(None, description="2FA enabled")

    # Plan (for authenticated user)
    plan: Plan | None = Field(None, description="Subscription plan")

    # Site admin
    site_admin: bool = Field(default=False, description="Is site administrator")


class Organization(BaseModel):
    """Organization model."""

    id: str = Field(description="Organization ID")
    login: str = Field(description="Organization login")
    type: UserType = Field(default=UserType.ORGANIZATION, description="Type")

    # Profile
    name: str | None = Field(None, description="Display name")
    description: str | None = Field(None, description="Organization description")
    email: str | None = Field(None, description="Public email")
    blog: str | None = Field(None, description="Blog URL")
    location: str | None = Field(None, description="Location")
    company: str | None = Field(None, description="Company name (for enterprise)")

    # URLs
    url: str = Field(description="API URL")
    html_url: str = Field(description="Profile URL")
    avatar_url: str | None = Field(None, description="Avatar URL")
    gravatar_id: str | None = Field(None, description="Gravatar ID")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    # Stats
    public_repos_count: int = Field(
        default=0, ge=0, description="Public repositories count"
    )
    public_gists_count: int = Field(default=0, ge=0, description="Public gists count")
    followers_count: int = Field(default=0, ge=0, description="Followers count")
    following_count: int = Field(default=0, ge=0, description="Following count")

    # Members
    members_count: int | None = Field(None, ge=0, description="Members count")

    # Billing
    plan: Plan | None = Field(None, description="Subscription plan")

    # Settings
    default_repository_permission: str = Field(
        default="read", description="Default permission for new repos"
    )
    members_can_create_repos: bool = Field(
        default=True, description="Members can create repositories"
    )
    members_can_create_public_repos: bool = Field(
        default=True, description="Members can create public repositories"
    )
    members_can_create_private_repos: bool = Field(
        default=True, description="Members can create private repositories"
    )
    two_factor_requirement_enabled: bool | None = Field(
        None, description="2FA required for all members"
    )


class OrgMembership(BaseModel):
    """Organization membership model."""

    id: str = Field(description="Membership ID")
    state: str = Field(description="Membership state (active/pending)")
    role: str = Field(description="Member role (admin/member/billing_manager)")
    organization_id: str = Field(description="Organization ID")
    organization_login: str = Field(description="Organization login")
    user_id: str = Field(description="User ID")
    user_username: str = Field(description="Username")
    created_at: datetime = Field(description="Membership created timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
