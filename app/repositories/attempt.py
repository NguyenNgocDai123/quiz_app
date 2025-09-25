from sqlalchemy.orm import Session
from uuid import UUID
from app.models.models import (
    QuizAttempt,
    QuizAttemptAnswer,
    QuizQuestion,
    QuestionOption,
    CourseQuiz,
)


def get_quiz(db: Session, quiz_id: UUID):
    return db.query(CourseQuiz).filter(CourseQuiz.id == quiz_id).first()


def count_user_attempts(db: Session, user_id: UUID, quiz_id: UUID) -> int:
    return (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == user_id, QuizAttempt.quiz_id == quiz_id)
        .count()
    )


def create_attempt(db: Session, attempt: QuizAttempt) -> QuizAttempt:
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def get_attempt(db: Session, attempt_id: UUID) -> QuizAttempt | None:
    return db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()


def save_answer(db: Session, answer: QuizAttemptAnswer):
    db.add(answer)


def commit(db: Session):
    db.commit()


def get_question(db: Session, question_id: UUID):
    return db.query(
        QuizQuestion).filter(QuizQuestion.id == question_id).first()


def get_option(db: Session, option_id: UUID):
    return db.query(
        QuestionOption).filter(QuestionOption.id == option_id).first()


def list_attempts(
    db: Session, user_id: UUID | None = None, quiz_id: UUID | None = None
):
    query = db.query(QuizAttempt)
    if user_id:
        query = query.filter(QuizAttempt.user_id == user_id)
    if quiz_id:
        query = query.filter(QuizAttempt.quiz_id == quiz_id)
    return query
