# app/repositories/course.py
from sqlalchemy.orm import Session
from app.models.models import Course
from app.schemas.course import CourseCreate, CourseUpdate
from uuid import UUID
from app.models.models import CourseEnrollment


def get_course_by_name(db: Session, name: str):
    return db.query(Course).filter(Course.name == name).first()


def get_course_by_code(db: Session, code: str):
    return db.query(Course).filter(Course.code == code).first()


def get_courses(db: Session):
    return db.query(Course)


def get_course_by_id(db: Session, course_id: UUID):
    return db.query(Course).filter(Course.id == course_id).first()


def get_enrolled_courses(db: Session, user_id: UUID):
    return (
        db.query(Course)
        .join(CourseEnrollment)
        .filter(CourseEnrollment.user_id == user_id)
    )


def get_enrollment(
    db: Session, course_id: UUID, user_id: UUID
) -> CourseEnrollment | None:
    return (
        db.query(CourseEnrollment)
        .filter(
            CourseEnrollment.course_id == course_id,
            CourseEnrollment.user_id == user_id
        )
        .first()
    )


def create_enrollment(
        db: Session, enrollment: CourseEnrollment
) -> CourseEnrollment:
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def create_course(db: Session, course_in: CourseCreate):
    course = Course(**course_in.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def update_course(db: Session, course: Course, course_in: CourseUpdate):
    for field, value in course_in.dict(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course: Course):
    db.delete(course)
    db.commit()
    return True
