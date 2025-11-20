from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List


class QuizAttemptCreate(BaseModel):
    user_id: UUID
    quiz_id: UUID


class QuizAttemptAnswerCreate(BaseModel):
    question_id: UUID
    option_id: UUID | None = None


class QuizAttemptResponse(BaseModel):
    id: UUID
    user_id: UUID
    quiz_id: UUID
    attempt_number: int
    score: float | None    # ✅ score có thể là float (thang 10)
    started_at: datetime
    finished_at: datetime | None

    class Config:
        orm_mode = True


class QuizAttemptAnswerResponse(BaseModel):
    id: UUID
    attempt_id: UUID
    question_id: UUID
    option_id: UUID | None
    is_correct: bool
    score: int

    class Config:
        orm_mode = True


class QuizAttemptDetailResponse(QuizAttemptResponse):
    total_questions: int          # ✅ tổng số câu hỏi
    correct_count: int            # ✅ số câu đúng
    answers: list[QuizAttemptAnswerResponse] = []


class QuizAttemptItem(BaseModel):
    attempt_id: str
    attempt_number: int
    score: int | None
    started_at: str
    finished_at: str | None

    class Config:
        orm_mode = True


class QuizAttemptByUser(BaseModel):
    user_id: str
    user_name: str
    attempts: List[QuizAttemptItem]

    class Config:
        orm_mode = True