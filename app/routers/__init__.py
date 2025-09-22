from fastapi import APIRouter
from app.routers import user, course, quiz, attempt, auth

api_router = APIRouter()

# Đăng ký tất cả router
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
# api_router.include_router(course.router, prefix="/courses", tags=["Courses"])
# api_router.include_router(quiz.router, prefix="/quizzes", tags=["Quizzes"])
# api_router.include_router(
#     attempt.router, prefix="/attempts", tags=["Attempts"])
