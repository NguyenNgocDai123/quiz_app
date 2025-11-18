# app/services/course.py
import random
import string
from sqlalchemy.orm import Session
from app.schemas.course import CourseCreate, CourseUpdate
from app.repositories import course as repo
from uuid import UUID
from fastapi import HTTPException
from datetime import datetime
from app.models.models import CourseEnrollment
from app.schemas.course import CourseOut


def list_courses(db: Session, page: int = 1, page_size: int = 10):
    query = repo.get_courses(db)
    total_items = query.count()
    total_page = (total_items + page_size - 1) // page_size
    offset = (page - 1) * page_size
    courses = query.offset(offset).limit(page_size).all()

    # Chuyển sang CourseOut có thêm member_count & quiz_count
    course_list = []
    for c in courses:
        course_list.append(
            CourseOut(
                id=c.id,
                name=c.name,
                code=c.code,
                teacher_id=c.teacher_id,
                created_at=c.created_at,
                member_count=len(
                    c.enrollments) if hasattr(c, "enrollments") else 0,
                quiz_count=len(c.quizzes) if hasattr(c, "quizzes") else 0,
            )
        )

    return {
        "page": page,
        "page_size": page_size,
        "total_page": total_page,
        "total_items": total_items,
        "next": page + 1 if page < total_page else None,
        "data": course_list,
    }


def list_enrolled_courses(
        db: Session, page: int = 1, page_size: int = 10, user_id: UUID = None):

    if not user_id:
        raise ValueError("User ID is required for enrolled courses")
    
    # Lấy query courses mà user đã enroll
    query = repo.get_enrolled_courses(db, user_id)
    total_items = query.count()
    total_page = (total_items + page_size - 1) // page_size
    offset = (page - 1) * page_size
    courses = query.offset(offset).limit(page_size).all()

    # Chuyển sang CourseOut có thêm member_count & quiz_count
    course_list = []
    for c in courses:
        course_list.append(
            CourseOut(
                id=c.id,
                name=c.name,
                code=c.code,
                teacher_id=c.teacher_id,
                created_at=c.created_at,
                member_count=len(c.enrollments) if hasattr(
                    c, "enrollments") else 0,
                quiz_count=len(c.quizzes) if hasattr(c, "quizzes") else 0,
            )
        )

    return {
        "page": page,
        "page_size": page_size,
        "total_page": total_page,
        "total_items": total_items,
        "next": page + 1 if page < total_page else None,
        "data": course_list,
    }


def get_course(db: Session, course_id: UUID):
    return repo.get_course_by_id(db, course_id)


def generate_course_code(length: int = 6) -> str:
    """Sinh mã khóa học ngẫu nhiên, ví dụ: COURSE-A1B2C3"""
    random_part = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=length))
    return f"COURSE-{random_part}"


def create_course_service(db: Session, course_in: CourseCreate):
    # Check trùng name
    existing_name = repo.get_course_by_name(db, course_in.name)
    if existing_name:
        raise HTTPException(
            status_code=400, detail="Course name already exists")

    # Sinh code random và đảm bảo không trùng
    code = generate_course_code()
    while repo.get_course_by_code(db, code):
        code = generate_course_code()

    # Gán code vào course_in
    course_in.code = code

    # Tạo mới
    course = repo.create_course(db, course_in)

    # Trả về kết quả
    return CourseOut(
        id=course.id,
        name=course.name,
        code=course.code,
        teacher_id=course.teacher_id,
        created_at=course.created_at,
        member_count=0,
        quiz_count=0
    )


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


def kick_student_from_course(
    db: Session, teacher_id: str, course_id: str, student_id: str
):
    # 1. Lấy khóa học
    course = repo.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 2. Kiểm tra xem caller có phải là giáo viên khóa học
    if str(course.teacher_id) != str(teacher_id):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to remove students from this course"
        )

    # 3. Tìm enrollment
    enrollment = repo.get_enrollment(db, course_id, student_id)
    if not enrollment:
        raise HTTPException(
            status_code=400,
            detail="Student is not enrolled in this course"
        )

    # 4. Xóa enrollment
    repo.delete_enrollment(db, enrollment)

    return {"message": "Student removed successfully"}