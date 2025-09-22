from typing_extensions import TypedDict


class Code(TypedDict):
    code: int
    message: str


class StatusCode:
    #  User
    SUCCESS: Code = Code(code=200, message="Success")
    NOT_FOUND: Code = Code(code=404, message="Not Found")
    UNAUTHORIZED: Code = Code(code=401, message="Unauthorized")
    FORBIDDEN: Code = Code(code=403, message="Forbidden")
    BAD_REQUEST: Code = Code(code=400, message="Bad Request")
    INTERNAL_SERVER_ERROR: Code = Code(code=500, message="Internal Server Error")
    SERVICE_UNAVAILABLE: Code = Code(code=503, message="Service Unavailable")
    GATEWAY_TIMEOUT: Code = Code(code=504, message="Gateway Timeout")
    CONFLICT: Code = Code(code=409, message="Conflict")
    UNPROCESSABLE_ENTITY: Code = Code(code=422, message="Unprocessable Entity")
    CREATED: Code = Code(code=201, message="Created")
    ACCEPTED: Code = Code(code=202, message="Accepted")
    NO_CONTENT: Code = Code(code=204, message="No Content")
    RESET_CONTENT: Code = Code(code=205, message="Reset Content")

    @classmethod
    def get_message(cls, code: int) -> str:
        """
        Retrieves the message corresponding to a given status code.

        Args:
            code (int): The status code to retrieve the message for.

        Returns:
            str: The message associated with the status code, or "Unknown Status Code" if not found.
        """
        for attr in cls.__annotations__.keys():
            if getattr(cls, attr)["code"] == code:
                return getattr(cls, attr)["message"]
        return "Unknown Status Code"
