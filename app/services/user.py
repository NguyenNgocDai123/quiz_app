from sqlalchemy.orm import Session
from uuid import UUID
from app.models.models import AppUser
import app.repositories.user
import app.schemas.user
import hashlib


def get_all_users_service(db: Session):
    return app.repositories.user.get_all_users(db)


def get_user_by_id_service(db: Session, user_id: UUID):
    return app.repositories.user.get_user_by_id(db, user_id)


def create_user_service(db: Session, user_in: app.schemas.user.UserCreate):
    hashed_pw = hashlib.sha256(user_in.password.encode()).hexdigest()
    user = AppUser(
        full_name=user_in.full_name,
        email=user_in.email,
        password=hashed_pw,
    )
    return app.repositories.user.create_user(db, user)


def update_user_service(
        db: Session, user_id: UUID,
        user_in: app.schemas.user.UserUpdate):

    db_user = app.repositories.user.get_user_by_id(db, user_id)
    if not db_user:
        return None
    updates = user_in.dict(exclude_unset=True)
    if "password" in updates:
        updates["password"] = hashlib.sha256(
            updates["password"].encode()).hexdigest()
    return app.repositories.user.update_user(db, db_user, updates)


def delete_user_service(db: Session, user_id: UUID):
    db_user = app.repositories.user.get_user_by_id(db, user_id)
    if not db_user:
        return None
    return app.repositories.user.delete_user(db, db_user)
