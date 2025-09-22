from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.database.session import get_db
from app.services.auth import login_service, refresh_token_service, logout_service
from fastapi.security import OAuth2PasswordBearer
from fastapi import Header

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_service(db, payload.full_name, payload.password)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_token_service(db, payload.refresh_token)


@router.post("/logout")
def logout(authorization: str = Header(...), db: Session = Depends(get_db)):
    # authorization = "Bearer <access_token>"
    token = authorization.split(" ")[1]
    from app.core.jwt import decode_token
    payload = decode_token(token)
    user_id = payload.get("sub")
    logout_service(db, user_id)
    return {"message": "Logged out successfully"}
