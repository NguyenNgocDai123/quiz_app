from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.session import get_db
from app.schemas.attempt import (
    QuizAttemptCreate,
    QuizAttemptAnswerCreate,
    QuizAttemptResponse,
    QuizAttemptDetailResponse,
    QuizAttemptByUser,
)
from app.services import attempt as service
from app.dependencies.dependencies import get_current_user
from app.models.models import AppUser
from app.common.pagination import PaginationResponse, PaginationRequest


router = APIRouter(prefix="/attempts", tags=["Attempts"])


@router.get("/by_quiz/{quiz_id}",
            response_model=PaginationResponse[QuizAttemptByUser])
def get_quiz_attempts_by_quiz(
    quiz_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    """
    Lấy danh sách học sinh có phân trang,
    kèm tất cả lần làm bài của từng học sinh
    """
    pagination = PaginationRequest(page=page, page_size=page_size)
    return service.get_attempts_grouped_by_user_paginated(
        db, quiz_id, pagination
    )


@router.post("/", response_model=QuizAttemptResponse)
def start_attempt(
    payload: QuizAttemptCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    return service.start_attempt(payload, db)


@router.post("/{attempt_id}/submit", response_model=QuizAttemptDetailResponse)
def submit_attempt(
    attempt_id: UUID,
    answers: list[QuizAttemptAnswerCreate],
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    return service.submit_attempt(attempt_id, answers, db)


@router.get("/{attempt_id}", response_model=QuizAttemptDetailResponse)
def get_attempt(
    attempt_id: UUID,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    return service.get_attempt(attempt_id, db)


@router.get("/", response_model=PaginationResponse[QuizAttemptResponse])
def list_attempts(
    user_id: UUID | None = None,
    quiz_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100,
                           description="Number of items per page"),
):
    return service.list_attempts(user_id, quiz_id, db, page, page_size)
