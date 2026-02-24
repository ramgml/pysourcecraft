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


class ProfileVisibility(str, Enum):
    """Profile visibility enum."""

    PRIVATE = "private"
    PUBLIC = "public"


class Location(BaseModel):
    """User location information."""

    country: str | None = Field(None, description="Country name")
    city: str | None = Field(None, description="City name")


class Timezone(BaseModel):
    """User timezone information."""

    iana_timezone: str | None = Field(None, description="IANA timezone identifier")


class Workplace(BaseModel):
    """User workplace information."""

    company: str | None = Field(None, description="Company name")
    position: str | None = Field(None, description="Job position")


class ProfileStatus(BaseModel):
    """User profile status."""

    message: str | None = Field(None, description="Status message")
    emoji: str | None = Field(None, description="Status emoji")


class Image(BaseModel):
    """Image reference."""

    url: str | None = Field(None, description="Image URL")


class Link(BaseModel):
    """External link."""

    link: str | None = Field(None, description="URL")
    type: str | None = Field(None, description="Link type")


class Plan(BaseModel):
    """User/Organization plan (kept for backward compatibility)."""

    name: str = Field(description="Plan name")
    space: int = Field(description="Storage space")
    private_repos: int = Field(description="Private repositories limit")
    collaborators: int = Field(description="Collaborators limit")


class UserEmbedded(BaseModel):
    """Minimal user reference (embedded in other models).

    Matches swagger schema UserEmbedded definition.
    """

    id: str = Field(description="User ID")
    slug: str = Field(description="User slug/username")


class UserProfile(BaseModel):
    """User profile model matching the API schema.

    This is returned by /users/{user_slug}, /users/id:{user_id}, etc.
    Matches swagger schema UserProfile definition.
    """

    id: str = Field(description="User ID")
    display_name: str | None = Field(None, description="Display name")
    username: str | None = Field(None, description="Username")
    bio: str | None = Field(None, description="User bio")

    # Location and timezone
    location: Location | None = Field(None, description="User location")
    timezone: Timezone | None = Field(None, description="User timezone")

    # Work info
    workplace: Workplace | None = Field(None, description="User workplace")

    # Links
    links: list[Link] = Field(default_factory=list, description="External links")

    # Status
    status: ProfileStatus | None = Field(None, description="Profile status")

    # Images
    avatar: Image | None = Field(None, description="Avatar image")
    background_image: Image | None = Field(None, description="Background image")

    # Visibility
    visibility: ProfileVisibility | None = Field(None, description="Profile visibility")


# For backward compatibility - User is now an alias for UserProfile
# since the API returns UserProfile for user endpoints
User = UserProfile


class OrganizationEmbedded(BaseModel):
    """Minimal organization reference (embedded in other models).

    Matches swagger schema OrganizationEmbedded definition.
    """

    id: str = Field(description="Organization ID")
    slug: str = Field(description="Organization slug")


class Organization(BaseModel):
    """Organization model.

    Note: The API uses OrganizationEmbedded for most references.
    This model provides additional organization details not fully defined
    in the swagger schema but used by the client.
    """

    id: str = Field(description="Organization ID")
    login: str = Field(description="Organization login/slug")
    type: UserType = Field(default=UserType.ORGANIZATION, description="Type")

    # Profile
    name: str | None = Field(None, description="Display name")
    description: str | None = Field(None, description="Organization description")
    email: str | None = Field(None, description="Public email")
    blog: str | None = Field(None, description="Blog URL")
    location: str | None = Field(None, description="Location")
    company: str | None = Field(None, description="Company name (for enterprise)")

    # URLs
    url: str | None = Field(None, description="API URL")
    html_url: str | None = Field(None, description="Profile URL")
    avatar_url: str | None = Field(None, description="Avatar URL")
    gravatar_id: str | None = Field(None, description="Gravatar ID")

    # Timestamps
    created_at: datetime | None = Field(None, description="Creation timestamp")
    updated_at: datetime | None = Field(None, description="Last update timestamp")

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
