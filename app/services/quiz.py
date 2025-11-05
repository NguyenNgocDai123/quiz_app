from sqlalchemy.orm import Session
from uuid import UUID

from app.repositories import quiz as quiz_repository
from app.schemas.quiz import (
    QuizCreate,
    QuizUpdate,
    QuestionCreate,
    QuestionResponse,
    QuizResponse,
)
from typing import List
from app.models.models import CourseQuiz, QuizAttempt
from app.common.pagination import PaginationResponse


def create_quiz(db: Session, quiz_in: QuizCreate, user_id: UUID) -> CourseQuiz:
    return quiz_repository.create_quiz(db, quiz_in, user_id)


def add_questions_to_quiz(
    db: Session, quiz_id: UUID, questions: List[QuestionCreate]
) -> List[QuestionResponse]:
    # Ở đây có thể thêm logic validate quiz tồn tại
    return quiz_repository.add_questions_to_quiz(db, quiz_id, questions)


def get_quiz(db: Session, quiz_id: UUID) -> CourseQuiz:
    return quiz_repository.get_quiz(db, quiz_id)


def list_quizzes(
    db: Session,
    course_id: UUID,
    user_id: UUID,  # Thêm user_id vào tham số
    page: int = 1,
    page_size: int = 10,
) -> PaginationResponse:  # Thay đổi kiểu trả về

    # 1. Tạo subquery để lấy finished_at của lần thử gần nhất cho user và quiz
    latest_attempt_subquery = (
        db.query(QuizAttempt.finished_at)
        .filter(
            QuizAttempt.quiz_id == CourseQuiz.id,  # Liên kết với quiz chính
            QuizAttempt.user_id == user_id,  # Lọc theo user hiện tại
        )
        .order_by(QuizAttempt.attempt_number.desc())
        .limit(1)
        .scalar_subquery()  # Trả về một giá trị duy nhất hoặc NULL
    )

    # 2. Lấy query cơ bản từ repository
    base_query = quiz_repository.list_quizzes(db, course_id)

    # 3. Thêm cột từ subquery vào query chính
    query_with_status = base_query.add_columns(
        latest_attempt_subquery.label("latest_attempt_finished_at")
    )

    # 4. Tính toán phân trang
    total_items = query_with_status.count()  # Đếm tổng số quiz
    total_page = (total_items + page_size - 1) // page_size
    offset = (page - 1) * page_size

    # 5. Thực thi query với phân trang
    # Kết quả sẽ là một list các tuple: (CourseQuiz_object, finished_at_value)
    items_with_status = query_with_status.offset(offset).limit(page_size).all()

    # 6. Xử lý kết quả để tạo response
    data = []
    for quiz, finished_at in items_with_status:
        # Chuyển đổi object SQLAlchemy thành dict
        quiz_dict = quiz.__dict__.copy()
        # Thêm thông tin từ subquery
        quiz_dict["latest_attempt_finished_at"] = finished_at
        # Tạo Pydantic model từ dict
        data.append(QuizResponse(**quiz_dict))

    return PaginationResponse(
        page=page,
        page_size=page_size,
        total_page=total_page,
        total_items=total_items,
        next=page + 1 if page < total_page else None,
        data=data,
    )


def get_questions_by_quiz(
    db: Session, quiz_id: UUID, page: int, page_size: int
) -> PaginationResponse[QuestionResponse]:
    query = quiz_repository.repo_get_questions(db, quiz_id)
    total_items = query.count()
    total_page = (total_items + page_size - 1) // page_size
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    return {
        "page": page,
        "page_size": page_size,
        "total_page": total_page,
        "total_items": total_items,
        "next": page + 1 if page < total_page else None,
        "data": items,
    }


def update_quiz(db: Session, quiz_id: UUID, quiz_in: QuizUpdate) -> CourseQuiz:
    quiz = get_quiz(db, quiz_id)
    return quiz_repository.update_quiz(db, quiz, quiz_in)


def delete_quiz(db: Session, quiz_id: UUID):
    quiz = get_quiz(db, quiz_id)
    quiz_repository.delete_quiz(db, quiz)
    return {"message": "Quiz deleted successfully"}
