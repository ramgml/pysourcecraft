"""SourceCraft API Client."""

from pysourcecraft.client import SourceCraftClient
from pysourcecraft.models import (
    BaseModel,
    PaginationParams,
    PaginatedResponse,
    ErrorResponse,
    APIError,
)
from pysourcecraft.models import (
    Run,
    RunList,
    RunWorkflowsRequest,
    GetCubeLogsResponse,
    GetCubeArtifactsResponse,
)

__version__ = "0.1.7"
__all__ = [
    "SourceCraftClient",
    "BaseModel",
    "PaginationParams",
    "PaginatedResponse",
    "ErrorResponse",
    "APIError",
    "Run",
    "RunList",
    "RunWorkflowsRequest",
    "GetCubeLogsResponse",
    "GetCubeArtifactsResponse",
]
