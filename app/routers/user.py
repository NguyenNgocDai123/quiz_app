from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
import app.services.user
import app.schemas.user
from uuid import UUID
from app.common.exceptions import BusinessException
from app.constants.business_code import BusinessCode
from app.common.pagination import PaginationResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=PaginationResponse[app.schemas.user.UserOut])
def get_all_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    return app.services.user.get_all_users_service(
        db, page=page, page_size=page_size)


@router.get("/{user_id}", response_model=app.schemas.user.UserOut)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    user = app.services.user.get_user_by_id_service(db, user_id)
    if not user:
        raise BusinessException(
            BusinessCode.USER_NOT_FOUND["code"],
            BusinessCode.USER_NOT_FOUND["message"],
            )
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
