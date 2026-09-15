import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.common import DataResponse


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: str = Field(..., min_length=2, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime
    last_login_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthResponseData(BaseModel):
    user: UserResponse
    token: AuthToken


class AuthResponse(DataResponse[AuthResponseData]):
    pass
