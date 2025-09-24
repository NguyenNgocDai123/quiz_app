from fastapi import APIRouter, Depends, HTTPException
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
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_service(db, payload.full_name, payload.password)


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
