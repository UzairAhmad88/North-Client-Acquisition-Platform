from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int = Field(default=1, ge=1, description="Current page number")
    page_size: int = Field(default=25, ge=1, le=100, description="Items per page")
    total: int = Field(default=0, ge=0, description="Total number of items")
    total_pages: int = Field(default=0, ge=0, description="Total number of pages")


class DataResponse(BaseModel, Generic[T]):
    data: T


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    pagination: PaginationMeta


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
