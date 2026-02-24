"""Base Pydantic models for SourceCraft API."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

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
    """Paginated response wrapper."""

    data: list[T] = Field(description="List of items")
    total: int = Field(ge=0, description="Total number of items")
    page: int = Field(ge=1, description="Current page number")
    per_page: int = Field(ge=1, description="Items per page")
    total_pages: int = Field(ge=0, description="Total number of pages")

    @property
    def has_next(self) -> bool:
        """Check if there is a next page."""
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        """Check if there is a previous page."""
        return self.page > 1


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
