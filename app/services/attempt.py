from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException

from app.models.models import QuizAttempt, QuizAttemptAnswer
from app.schemas.attempt import QuizAttemptCreate, QuizAttemptAnswerCreate
from app.repositories import attempt as repo


def start_attempt(payload: QuizAttemptCreate, db: Session) -> QuizAttempt:
    quiz = repo.get_quiz(db, payload.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    prev_attempts = repo.count_user_attempts(
        db, payload.user_id, payload.quiz_id
    )

    attempt = QuizAttempt(
        user_id=payload.user_id,
        quiz_id=payload.quiz_id,
        attempt_number=prev_attempts + 1,
        started_at=datetime.utcnow(),
    )
    return repo.create_attempt(db, attempt)


def submit_attempt(
    attempt_id: UUID,
    answers: list[QuizAttemptAnswerCreate],
    db: Session
) -> QuizAttempt:
    attempt = repo.get_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.finished_at:
        raise HTTPException(
            status_code=400, detail="Attempt already submitted"
        )

    total_score = 0
    for ans in answers:
        question = repo.get_question(db, ans.question_id)
        if not question:
            continue

        option = repo.get_option(db, ans.option_id) if ans.option_id else None
        is_correct = option.is_correct if option else False
        score = 1 if is_correct else 0
        total_score += score

        attempt_answer = QuizAttemptAnswer(
            attempt_id=attempt.id,
            question_id=ans.question_id,
            option_id=ans.option_id,
            is_correct=is_correct,
            score=score,
        )
        repo.save_answer(db, attempt_answer)

    attempt.score = total_score
    attempt.finished_at = datetime.utcnow()
    repo.commit(db)
    db.refresh(attempt)

    return attempt


def get_attempt(attempt_id: UUID, db: Session) -> QuizAttempt:
    attempt = repo.get_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt


def list_attempts(
    user_id: UUID | None,
    quiz_id: UUID | None,
    db: Session,
    page: int = 1,
    page_size: int = 10
):
    query = repo.list_attempts(db, user_id, quiz_id)
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
