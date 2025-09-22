from fastapi import FastAPI
from app.routers import api_router

app = FastAPI(
    title="QuizMaster API",
    version="1.0.0"
)

app.include_router(api_router)
