from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import AppUser
from app.core.jwt import decode_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Thử parse UUID
        try:
            user_uuid = UUID(user_id)
            print("Parsed UUID:", user_uuid)
            user = db.query(AppUser).filter(AppUser.id == user_uuid).first()
            print("User found by UUID:", user.id if user else "None")
        except ValueError:
            # Nếu không phải UUID, tìm theo username hoặc email
            user = db.query(AppUser).filter(
                (AppUser.full_name == user_id) | (AppUser.email == user_id)
            ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        print("Authenticated user:", user.full_name)
        return user

    except Exception as e:
        print("Token decode error:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
