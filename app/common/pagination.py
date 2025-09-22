from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class PaginationRequest(BaseModel):
    """
    Common schema for pagination requests.
    """
    page: int = Field(1, ge=1, description="The current page number (default: 1).")
    page_size: int = Field(10, ge=1, le=100, description="The number of records per page (default: 10).")


T = TypeVar("T")


class PaginationResponse(BaseModel, Generic[T]):
    """
    Common schema for paginated responses.
    """

    page: int | None = Field(
        None, description="The current page number of the paginated result.", example=1
    )
    page_size: int | None = Field(None, description="The number of items per page.", example=10)
    total_page: int | None = Field(None, description="The total number of pages.", example=5)
    total_items: int | None = Field(None, description="The total number of items.", example=50)
    next: int | None = Field(
        None, description="The next page number if available.", example=2
    )
    data: list[T] = Field(..., description="List of items on the current page.")
