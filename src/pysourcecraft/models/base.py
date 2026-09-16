"""Base Pydantic models for SourceCraft API."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, model_validator

T = TypeVar("T")


class BaseModel(PydanticBaseModel):
    """Base model with common configuration."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="ignore",
    )


class PaginationParams(BaseModel):
    """Pagination parameters for list requests."""

    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    per_page: int = Field(
        default=30, ge=1, le=100, description="Number of items per page"
    )

    def to_query_params(self) -> dict[str, Any]:
        """Convert to query parameters dictionary."""
        return {
            "page": self.page,
            "per_page": self.per_page,
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper.

    The API returns the SourceCraft list shape: ``{"<items>": [...],
    "next_page_token": "..."}`` (sourcecraft.swagger.json, e.g.
    ListRepositoryPullRequestsResponse). The legacy page-numbered shape
    (``data``/``total``/``page``/``per_page``/``total_pages``) is accepted
    for backward compatibility but is never produced by the live API.
    """

    data: list[T] = Field(default_factory=list, description="List of items")
    next_page_token: str | None = Field(
        None, description="Token for the next page; None/empty = last page"
    )
    # Legacy page-numbered fields (kept for backward compatibility with
    # code that reads them; the live API does not send them).
    total: int | None = Field(None, ge=0)
    page: int | None = Field(None, ge=1)
    per_page: int | None = Field(None, ge=1)
    total_pages: int | None = Field(None, ge=0)

    @model_validator(mode="wrap")
    @classmethod
    def _fold_resource_items(cls, values: Any, handler: Any) -> PaginatedResponse[T]:
        """Accept the SourceCraft list shape: the items array arrives under
        a resource-specific key (pull_requests, releases, issues, ...);
        fold any list value into ``data`` before validation."""
        if isinstance(values, dict) and "data" not in values:
            items = None
            for key in (
                "pull_requests",
                "releases",
                "issues",
                "repositories",
                "workflows",
                "workflow_runs",
                "pipelines",
                "artifacts",
                "comments",
                "branches",
                "users",
                "organizations",
            ):
                v = values.get(key)
                if isinstance(v, list):
                    items = v
                    break
            if items is not None:
                values = dict(values)
                values["data"] = items
        return handler(values)

    @property
    def has_next(self) -> bool:
        """Check if there is a next page.

        Token-based API: a non-empty next_page_token means more pages.
        Legacy page-numbered payloads fall back to page/total_pages.
        """
        if self.next_page_token:
            return True
        if self.page is not None and self.total_pages is not None:
            return self.page < self.total_pages
        return False

    @property
    def has_prev(self) -> bool:
        """Check if there is a previous page (legacy numbered payloads)."""
        return self.page is not None and self.page > 1


class ErrorResponse(BaseModel):
    """API error response matching ApiErrorResponse from swagger.

    Schema from sourcecraft.swagger.json:
    - error_code: Error code that can be used for error handling
    - message: Human-readable message
    - request_id: Request ID for tracking
    - details: Optional details (structure depends on error_code)
    """

    error_code: str = Field(
        description="Error code that can be used for error handling"
    )
    message: str = Field(description="Human-readable message")
    request_id: str | None = Field(None, description="Request ID")
    details: dict[str, str] | None = Field(
        None, description="Optional details (structure depends on error_code)"
    )


class APIError(Exception):
    """Custom exception for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        error_response: ErrorResponse | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_response = error_response

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message
