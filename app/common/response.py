
from typing import Generic

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing_extensions import Any, TypedDict, TypeVar


T = TypeVar("T")


class AppResponseModel(BaseModel, Generic[T]):
    """
    A generic response model that wraps API responses in a standard format.
    """

    business_code: int | None = Field(
        default=None,
        description="Optional business-specific code for the response ("
        "e.g., custom error codes).",
    )
    status_code: int = Field(
        ...,
        description="HTTP status code of the response ("
        "e.g., 200 for success, 404 for not found).",
    )
    message: str = Field(
        ..., description=""
        "A human-readable message describing the response result."
    )
    data: T = Field(
        default=None,
        description="The actual payload of the response. "
        "Can be any type (e.g., object, list, etc.).",
    )

    class Config:
        from_attributes = True

    class ResponseInfo(TypedDict, total=False):
        model: type[Any]
        description: str

    @staticmethod
    def openapi_extra_responses(
        responses: dict[int, "AppResponseModel.ResponseInfo"],
    ) -> dict[str, Any]:
        result: dict[str, Any] = {"responses": {}}
        for code, info in responses.items():
            description = info.get("description", "")
            model = info.get("model")
            if model:
                full_model = AppResponseModel[model]
                schema = full_model.model_json_schema()
                result["responses"][code] = {
                    "description": description,
                    "content": {
                        "application/json": {"schema": schema}
                    },
                }
            else:
                result["responses"][code] = {"description": description}
        return result


class BusinessJsonResponse(JSONResponse):
    """
    A JSONResponse that includes a business code in the response headers.
    """

    header_business_code: str = "X-API-Business-Code"

    def __init__(
        self,
        business_code: int, content: Any, status_code: int = 200, **kwargs: Any
    ) -> None:
        """
        Initializes a BusinessJsonResponse with a business code in the headers.

        Args:
            business_code (int):
            The business code to include in the response headers.
            content (Any): The content of the response.
            status_code (int, optional): The status code of the response.
            Defaults to 200.
        """
        super().__init__(content=content, status_code=status_code, **kwargs)
        self.business_code = business_code
        self.headers[self.header_business_code] = str(business_code)
