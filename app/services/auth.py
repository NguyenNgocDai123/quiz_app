from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.models import AppUser
from app.constants.business_code import BusinessCode
from app.common.exceptions import BusinessException
from app.core.jwt import (
    create_access_token, create_refresh_token, decode_token)
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def login_service(db: Session, full_name: str, password: str):
    user = db.query(AppUser).filter(AppUser.full_name == full_name).first()
    if not user:
        raise BusinessException(BusinessCode.USER_NOT_FOUND["code"])
    if not user.is_active:
        raise BusinessException(BusinessCode.USER_NOT_ACTIVE["code"])
    if not verify_password(password, user.password):
        raise BusinessException(BusinessCode.USER_PASSWORD_INCORRECT["code"])

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Lưu refresh token vào DB hoặc cache (optional)
    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_token_service(db: Session, refresh_token: str):
    try:
        payload = decode_token(refresh_token)
    except Exception:
        raise HTTPException(
            status_code=401, detail="Invalid or expired refresh token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(AppUser).filter(AppUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 🚀 bỏ check user.refresh_token nếu không lưu DB
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Nếu có DB column refresh_token thì update, còn không thì bỏ dòng này
    # user.refresh_token = new_refresh_token
    # db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


def logout_service(db: Session, user_id: str):
    user = db.query(AppUser).filter(AppUser.id == user_id).first()
    if user:
        user.refresh_token = None
        db.commit()
