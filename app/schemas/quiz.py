from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.constants.enums.questionType import QuestionType


class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: UUID
    teacher_id: Optional[UUID] = None
    time_limit: Optional[int] = None
    max_attempts: Optional[int] = None
    total_points: Optional[int] = None
    is_published: bool = False


class QuizCreate(QuizBase):
    pass


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit: Optional[int] = None
    max_attempts: Optional[int] = None
    total_points: Optional[int] = None
    is_published: Optional[bool] = None


class QuizResponse(QuizBase):
    id: UUID
    created_at: datetime
    finished_at: Optional[datetime] = None
    attempt_count: Optional[int] = 0
    remaining_attempts: Optional[int] = 0
    latest_attempt_finished_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class QuestionOptionCreate(BaseModel):
    id: Optional[UUID] = None
    content: str
    is_correct: bool = False


class QuestionCreate(BaseModel):
    content: str
    type: str = QuestionType
    points: int = 1
    options: List[QuestionOptionCreate]


class QuestionResponse(QuestionCreate):
    id: UUID
    options: List[QuestionOptionCreate]

    class Config:
        orm_mode = True
