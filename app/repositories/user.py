from sqlalchemy.orm import Session
from app.models.models import AppUser
from uuid import UUID


def get_all_users(db: Session):
    return db.query(AppUser).all()


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(AppUser).filter(AppUser.id == user_id).first()


def create_user(db: Session, user: AppUser):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, db_user: AppUser, updates: dict):
    for field, value in updates.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: AppUser):
    db.delete(db_user)
    db.commit()
    return db_user
