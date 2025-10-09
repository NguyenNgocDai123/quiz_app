from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api_router
from app.middlewares.exception_handle import (
    BusinessException,
    IntegrityError,
    RequestValidationError,
    handler_business_exception,
    handler_sqlalchemy_exception,
    handler_unknown_exception,
    handler_validation_exception,
)
from app.middlewares.response_wrapper import ResponseWrapperMiddleware

app = FastAPI(title="QuizMaster API", version="1.0.0")

# CORS middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler

app.add_exception_handler(BusinessException, handler_business_exception)
app.add_exception_handler(RequestValidationError, handler_validation_exception)
app.add_exception_handler(IntegrityError, handler_sqlalchemy_exception)
app.add_exception_handler(Exception, handler_unknown_exception)

# Response wrapper middleware

app.add_middleware(ResponseWrapperMiddleware)

# Routers

app.include_router(api_router)
