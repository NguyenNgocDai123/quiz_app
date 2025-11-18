# app/api/v1/course.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.database.session import get_db
from app.schemas.course import (
    CourseCreate, CourseUpdate, CourseOut, CourseEnrollmentOut)
from app.services import course as service
from app.dependencies.dependencies import get_current_user
from app.models.models import AppUser
from app.common.pagination import PaginationResponse

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=PaginationResponse[CourseOut])
def list_courses(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    return service.list_courses(db, page=page, page_size=page_size)


@router.get("/enrolled", response_model=PaginationResponse[CourseOut])
def list_enrolled_courses(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    user: AppUser = Depends(get_current_user),
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    return service.list_enrolled_courses(
        db, page=page, page_size=page_size, user_id=user.id
    )


@router.get("/{course_id}", response_model=CourseOut)
def get_course(
    course_id: UUID,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    course = service.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", response_model=CourseOut)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    return service.create_course_service(db, course_in)


@router.post("/join", response_model=CourseEnrollmentOut)
def join_course(
    course_code: str,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    enrollment = service.join_course_service(db, current_user.id, course_code)
    if not enrollment:
        raise HTTPException(status_code=400, detail="Cannot join course")
    return enrollment


@router.put("/{course_id}", response_model=CourseOut)
def update_course(
    course_id: UUID,
    course_in: CourseUpdate,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    course = service.update_course_service(db, course_id, course_in)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.delete("/{course_id}")
def delete_course(
    course_id: UUID,
    db: Session = Depends(get_db),
    _: AppUser = Depends(get_current_user),
):
    success = service.delete_course_service(db, course_id)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}


@router.delete("/{course_id}/kick/{student_id}")
def remove_student_from_course(
    course_id: str,
    student_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return service.kick_student_from_course(
        db=db,
        teacher_id=str(current_user.id),
        course_id=course_id,
        student_id=student_id,
    )
