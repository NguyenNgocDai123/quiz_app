from fastapi import APIRouter
from app.routers import user, course, quiz, attempt, auth, pdf_parser

api_router = APIRouter()

# Đăng ký tất cả router
api_router.include_router(user.router, prefix="/app", tags=["Users"])
api_router.include_router(auth.router, prefix="/app", tags=["Auth"])
api_router.include_router(course.router, prefix="/app", tags=["Courses"])
api_router.include_router(quiz.router, prefix="/app", tags=["Quizzes"])
api_router.include_router(
    pdf_parser.router, prefix="/app", tags=["PDF Parser"]
)
api_router.include_router(
    attempt.router, prefix="/app", tags=["Attempts"]
)
