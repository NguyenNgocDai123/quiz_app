from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
import app.services.user
import app.schemas.user
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[app.schemas.user.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return app.services.user.get_all_users_service(db)


@router.get("/{user_id}", response_model=app.schemas.user.UserOut)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    user = app.services.user.get_user_by_id_service(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=app.schemas.user.UserOut)
def create_user(
    user_in: app.schemas.user.UserCreate,
    db: Session = Depends(get_db)
):
    return app.services.user.create_user_service(db, user_in)


@router.put("/{user_id}", response_model=app.schemas.user.UserOut)
def update_user(
    user_id: UUID, 
    user_in: app.schemas.user.UserUpdate, 
    db: Session = Depends(get_db)
):
    user = app.services.user.update_user_service(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=app.schemas.user.UserOut)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = app.services.user.delete_user_service(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
