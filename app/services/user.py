from sqlalchemy.orm import Session
from math import ceil
from uuid import UUID
from app.models.models import AppUser
import app.repositories.user
import app.schemas.user
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all_users_service(db: Session, page: int = 1, page_size: int = 10):
    query = app.repositories.user.get_all_users(db)
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


def get_all_users_in_course(
    db: Session,
    course_id: str,
    page: int = 1,
    page_size: int = 10
):
    query = app.repositories.user.get_users_in_course(db, course_id)
    total_items = query.count()
    total_page = ceil(total_items / page_size)
    offset = (page - 1) * page_size

    users = query.offset(offset).limit(page_size).all()

    return {
        "page": page,
        "page_size": page_size,
        "total_page": total_page,
        "total_items": total_items,
        "next": page + 1 if page < total_page else None,
        "data": users
    }


def get_user_by_id_service(db: Session, user_id: UUID):
    return app.repositories.user.get_user_by_id(db, user_id)


def create_user_service(db: Session, user_in: app.schemas.user.UserCreate):
    # Hash password với bcrypt
    hashed_pw = pwd_context.hash(user_in.password)
    user = AppUser(
        full_name=user_in.full_name,
        email=user_in.email,
        password=hashed_pw,  # lưu vào cột password_hash
        is_active=True,
        role=user_in.role
    )
    return app.repositories.user.create_user(db, user)


def update_user_service(
    db: Session, user_id: UUID, user_in: app.schemas.user.UserUpdate
):
    db_user = app.repositories.user.get_user_by_id(db, user_id)
    if not db_user:
        return None

    updates = user_in.dict(exclude_unset=True)

    # Nếu có cập nhật password, hash bcrypt
    if "password" in updates:
        updates["password"] = pwd_context.hash(updates.pop("password"))

    return app.repositories.user.update_user(db, db_user, updates)


def delete_user_service(db: Session, user_id: UUID):
    db_user = app.repositories.user.get_user_by_id(db, user_id)
    if not db_user:
        return None
    return app.repositories.user.delete_user(db, db_user)
