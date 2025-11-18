from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException

from app.models.models import QuizAttempt, QuizAttemptAnswer, QuizQuestion
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
) -> dict:
    attempt = repo.get_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.finished_at:
        raise HTTPException(
            status_code=400, detail="Attempt already submitted"
        )

    # ✅ Lấy danh sách câu hỏi của quiz
    all_questions = (
        db.query(QuizQuestion)
        .filter(QuizQuestion.quiz_id == attempt.quiz_id)
        .all()
    )
    total_questions = len(all_questions)

    correct_count = 0

    # ✅ Chấm điểm từng câu
    for ans in answers:
        question = repo.get_question(db, ans.question_id)
        if not question:
            continue

        option = repo.get_option(db, ans.option_id) if ans.option_id else None
        is_correct = option.is_correct if option else False

        if is_correct:
            correct_count += 1

        attempt_answer = QuizAttemptAnswer(
            attempt_id=attempt.id,
            question_id=ans.question_id,
            option_id=ans.option_id,
            is_correct=is_correct,
            score=1 if is_correct else 0,
        )
        repo.save_answer(db, attempt_answer)

    # ✅ Tính điểm theo thang 10
    score = (correct_count / total_questions) * 10

    # ✅ Làm tròn 1 chữ số thập phân (tuỳ bạn)
    score = round(score, 1)

    attempt.score = score
    attempt.finished_at = datetime.utcnow()

    repo.commit(db)
    db.refresh(attempt)

    # ✅ Trả về đầy đủ dữ liệu
    return {
        "id": attempt.id,
        "quiz_id": attempt.quiz_id,
        "user_id": attempt.user_id,
        "attempt_number": attempt.attempt_number,
        "score": attempt.score,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "started_at": attempt.started_at,
        "finished_at": attempt.finished_at,
        "answers": attempt.answers,
    }


def get_attempt(attempt_id: UUID, db: Session) -> dict:
    attempt = repo.get_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    # ✅ Lấy danh sách câu hỏi thuộc quiz
    all_questions = (
        db.query(QuizQuestion)
        .filter(QuizQuestion.quiz_id == attempt.quiz_id)
        .all()
    )
    total_questions = len(all_questions)

    # ✅ Đếm số câu đúng
    correct_count = (
        db.query(QuizAttemptAnswer)
        .filter(
            QuizAttemptAnswer.attempt_id == attempt_id,
            QuizAttemptAnswer.is_correct == True
        )
        .count()
    )

    # ✅ Điểm (nếu attempt.score chưa tính)
    score = attempt.score
    if score is None:
        score = round((correct_count / total_questions) * 10, 1)

    return {
        "id": attempt.id,
        "quiz_id": attempt.quiz_id,
        "user_id": attempt.user_id,
        "attempt_number": attempt.attempt_number,
        "score": score,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "started_at": attempt.started_at,
        "finished_at": attempt.finished_at,
        "answers": attempt.answers,
    }


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
