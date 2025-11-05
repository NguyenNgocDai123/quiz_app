from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database.session import get_db
from app.schemas.quiz import (
    QuizCreate, QuizUpdate, QuizResponse, QuestionCreate, QuestionResponse)
from app.services import quiz as quiz_service
from app.dependencies.dependencies import get_current_user
from app.models.models import AppUser
from app.common.pagination import PaginationResponse
from app.models.models import RoleEnum

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.get("/course/{course_id}", 
            response_model=PaginationResponse[QuizResponse])
def list_quizzes(
    course_id: UUID,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, 
                           description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
    # Đổi tên biến cho rõ nghĩa
):
    """
    Lấy danh sách quiz trong 1 course (có phân trang)
    và trạng thái hoàn thành của người dùng hiện tại.
    """
    # Truyền current_user.id vào service
    return quiz_service.list_quizzes(
        db,
        course_id=course_id,
        user_id=current_user.id,
        page=page,
        page_size=page_size
    )


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: UUID,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    """
    Lấy chi tiết một quiz theo ID.
    """
    quiz = quiz_service.get_quiz(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.get("/{quiz_id}/questions",
            response_model=PaginationResponse[QuestionResponse])
def get_questions_by_quiz(
    quiz_id: UUID,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    """
    Lấy danh sách câu hỏi trong một quiz (có phân trang).
    """
    return quiz_service.get_questions_by_quiz(
        db, quiz_id=quiz_id, page=page, page_size=page_size
    )


@router.post("/", response_model=QuizResponse)
def create_quiz(
    quiz_in: QuizCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    """
    Tạo một quiz mới (giáo viên).
    """
    if not current_user.role == RoleEnum.TEACHER:
        raise HTTPException(status_code=403,
                            detail="Only teachers have the right to create")
    return quiz_service.create_quiz(db, quiz_in, current_user.id)


@router.post("/{quiz_id}/questions", response_model=List[QuestionResponse])
def add_questions(
    quiz_id: UUID,
    questions: List[QuestionCreate],
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    """
    Thêm nhiều câu hỏi vào quiz.
    Chỉ giáo viên mới có quyền.
    """
    if current_user.role != RoleEnum.TEACHER:
        raise HTTPException(status_code=403,
                            detail="Only teachers can add questions")

    return quiz_service.add_questions_to_quiz(db, quiz_id, questions)


@router.put("/{quiz_id}", response_model=QuizResponse)
def update_quiz(
    quiz_id: UUID,
    quiz_in: QuizUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    """
    Cập nhật thông tin quiz.
    """
    quiz = quiz_service.update_quiz(db, quiz_id, quiz_in)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.delete("/{quiz_id}")
def delete_quiz(
    quiz_id: UUID,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    """
    Xóa một quiz.
    """
    success = quiz_service.delete_quiz(db, quiz_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"message": "Quiz deleted successfully"}
