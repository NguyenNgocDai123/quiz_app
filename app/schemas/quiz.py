from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


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

    class Config:
        from_attributes = True


class QuestionOptionCreate(BaseModel):
    content: str
    is_correct: bool = False


class QuestionCreate(BaseModel):
    content: str
    type: str = "single_choice"
    points: int = 1
    options: List[QuestionOptionCreate]


class QuestionResponse(QuestionCreate):
    id: UUID
    options: List[QuestionOptionCreate]

    class Config:
        orm_mode = True
