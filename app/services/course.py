# app/services/course.py
from sqlalchemy.orm import Session
from app.schemas.course import CourseCreate, CourseUpdate
from app.repositories import course as repo
from uuid import UUID
from fastapi import HTTPException
from datetime import datetime
from app.models.models import CourseEnrollment


def list_courses(db: Session, page: int = 1, page_size: int = 10):
    query = repo.get_courses(db)
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


def get_course(db: Session, course_id: UUID):
    return repo.get_course_by_id(db, course_id)


def create_course_service(db: Session, course_in: CourseCreate):
    # check name
    existing_name = repo.get_course_by_name(db, course_in.name)
    if existing_name:
        raise HTTPException(
            status_code=400, detail="Course name already exists")

    # check code
    existing_code = repo.get_course_by_code(db, course_in.code)
    if existing_code:
        raise HTTPException(
            status_code=400, detail="Course code already exists")

    return repo.create_course(db, course_in)


def join_course_service(db: Session, user_id: UUID, course_code: str):
    # 🔍 Tìm course theo code
    course = repo.get_course_by_code(db, course_code)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 👀 Kiểm tra user đã tham gia chưa
    existing = repo.get_enrollment(db, course.id, user_id)
    if existing:
        raise HTTPException(status_code=400, detail="User already enrolled")

    # 📝 Tạo enrollment mới
    enrollment = CourseEnrollment(
        course_id=course.id,
        user_id=user_id,
        joined_at=datetime.utcnow()
    )
    return repo.create_enrollment(db, enrollment)


def update_course_service(
        db: Session,
        course_id: UUID,
        course_in: CourseUpdate):
    course = repo.get_course_by_id(db, course_id)
    if not course:
        return None
    return repo.update_course(db, course, course_in)


def delete_course_service(db: Session, course_id: UUID):
    course = repo.get_course_by_id(db, course_id)
    if not course:
        return None
    return repo.delete_course(db, course)
