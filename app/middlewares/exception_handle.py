import re
import traceback

import psycopg2
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.common.exceptions import BusinessException
from app.common.response import BusinessJsonResponse

# ANSI
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def handler_unknown_exception(
        request: Request, exc: Exception) -> JSONResponse:
    """
    Handles unknown exceptions by returning a JSONResponse with a status code
    and a JSON body containing the error message.

    Parameters:
        request (Request): The incoming request that triggered the exception.
        exc (Exception): The unknown exception that was raised.
    """
    tb_lines = "".join(
        traceback.format_exception(type(exc), exc, exc.__traceback__)
    ).splitlines()

    # Create a markdown report
    summary = [
        f"{RED}{BOLD} Internal Server Error{RESET}",
        f"{CYAN}Method:{RESET} {request.method}",
        f"{CYAN}Path:{RESET}   {request.url.path}",
        f"{YELLOW}Exception:{RESET} {exc}",
    ]

    rows = []
    rows.append({"Section": "[SUMMARY]", "Message": ""})
    for line in summary:
        rows.append({"Section": " ", "Message": line})
    rows.append({"Section": "[TRACEBACK]", "Message": ""})
    for line in tb_lines:
        rows.append({"Section": " ", "Message": line})

    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )


def handler_business_exception(
        _: Request, exc: BusinessException) -> JSONResponse:
    """
    Handles a BusinessException by returning a JSONResponse with a status code
    and a JSON body containing the error code and message.

    Parameters:
        request (Request): The incoming request that triggered the exception.
        exc (BusinessException): The BusinessException that was raised.

    Returns:
        JSONResponse:
        A JSONResponse with a status code and a JSON body containing
        the error code and message.
    """
    return BusinessJsonResponse(
        business_code=exc.business_code,
        status_code=400,
        content={"message": exc.message},
    )


def handler_validation_exception(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handles validation errors raised by FastAPI when input validation fails.

    Parameters:
        request (Request):
        The incoming request that caused the validation error.
        exc (RequestValidationError): The validation error that was raised.

    Returns:
        JSONResponse: A response with details of all validation issues.
    """
    errors = [
        {
            "field": err["loc"][-1],
            "msg": err["msg"],
            "type": err["type"],
        }
        for err in exc.errors()
    ]

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Validation error", "errors": errors},
    )


def handler_sqlalchemy_exception(
        _: Request, exc: IntegrityError) -> JSONResponse:
    """
    Handles SQLAlchemy IntegrityError (e.g. duplicate key).
    Extracts useful message from the DB error and returns in JSON format.
    """
    orig = getattr(exc, "orig", None)
    detail = ""

    if isinstance(orig, psycopg2.errors.UniqueViolation):
        message = str(orig)
        match = re.search(r"DETAIL:\s+(.*)", message)
        detail = match.group(1) if match else "Unique constraint violated"
    else:
        detail = str(orig) if orig else str(exc)

    return JSONResponse(
        status_code=400,
        content={"message": "Database error", "detail": detail},
    )
