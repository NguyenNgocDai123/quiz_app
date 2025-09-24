# app/schemas/course.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class CourseBase(BaseModel):
    name: str
    code: str
    teacher_id: Optional[UUID] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    teacher_id: Optional[UUID] = None


class CourseOut(CourseBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class CourseEnrollmentOut(BaseModel):
    id: UUID
    course_id: UUID
    user_id: UUID
    joined_at: datetime

    class Config:
        orm_mode = True
