from sqlalchemy.orm import Session
from uuid import UUID

from app.repositories import quiz as quiz_repository
from app.schemas.quiz import QuizCreate, QuizUpdate
from app.models.models import CourseQuiz


def create_quiz(db: Session, quiz_in: QuizCreate, user_id: UUID) -> CourseQuiz:
    return quiz_repository.create_quiz(db, quiz_in, user_id)


def get_quiz(db: Session, quiz_id: UUID) -> CourseQuiz:
    return quiz_repository.get_quiz(db, quiz_id)


def list_quizzes(
        db: Session, course_id: UUID,
        page: int = 1,
        page_size: int = 10
) -> list[CourseQuiz]:

    query = quiz_repository.list_quizzes(db, course_id)
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
        "data": items
    }


def update_quiz(db: Session, quiz_id: UUID, quiz_in: QuizUpdate) -> CourseQuiz:
    quiz = get_quiz(db, quiz_id)
    return quiz_repository.update_quiz(db, quiz, quiz_in)


def delete_quiz(db: Session, quiz_id: UUID):
    quiz = get_quiz(db, quiz_id)
    quiz_repository.delete_quiz(db, quiz)
    return {"message": "Quiz deleted successfully"}
