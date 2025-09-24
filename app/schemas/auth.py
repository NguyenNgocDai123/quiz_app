from pydantic import BaseModel


class LoginRequest(BaseModel):
    full_name: str
    password: str


class LogoutRequest(BaseModel):
    access_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str