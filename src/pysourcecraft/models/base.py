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


class ErrorDetail(BaseModel):
    """Error detail information."""

    field: str | None = Field(None, description="Field that caused the error")
    message: str = Field(description="Error message")
    code: str | None = Field(None, description="Error code")


class ErrorResponse(BaseModel):
    """API error response."""

    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    details: list[ErrorDetail] = Field(
        default_factory=list, description="Error details"
    )
    status_code: int = Field(description="HTTP status code")


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
