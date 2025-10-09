from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    LogoutRequest,
)
from app.database.session import get_db
from app.services.auth import (
    login_service, refresh_token_service, logout_service)
from app.core.jwt import decode_token

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    tokens = login_service(db, payload.full_name, payload.password)

    # Set cookies
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,  # ⚠️ Đặt True khi chạy HTTPS
        samesite="lax",
        max_age=60 * 15,  # 15 phút (giống exp access_token)
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 ngày (tuỳ config refresh_token)
    )

    # Trả về JSON nếu bạn cần (
    # có thể xoá access_token/refresh_token ở đây để bảo mật hơn)
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_token_service(db, payload.refresh_token)


@router.post("/logout")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    """
    Truyền access_token trong body request.
    Ví dụ body JSON:
    {
        "access_token": "<token_here>"
    }
    """
    token = payload.access_token

    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    logout_service(db, user_id)
    return {"message": "Logged out successfully"}
