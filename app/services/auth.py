from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.models import AppUser
from app.constants.business_code import BusinessCode
from app.common.exceptions import BusinessException
from app.core.jwt import create_access_token, create_refresh_token, decode_token

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

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


def refresh_token_service(db: Session, refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
    except Exception:
        raise BusinessException(BusinessCode.USER_TOKEN_INVALID["code"])

    user = db.query(AppUser).filter(AppUser.id == user_id).first()
    if not user or user.refresh_token != refresh_token:
        raise BusinessException(BusinessCode.USER_TOKEN_INVALID["code"])

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


def logout_service(db: Session, user_id: str):
    user = db.query(AppUser).filter(AppUser.id == user_id).first()
    if user:
        user.refresh_token = None
        db.commit()
