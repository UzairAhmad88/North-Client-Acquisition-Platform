from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserResponse,
)
from app.schemas.common import DataResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    auth_data = AuthService.register_user(db, data)
    return {"data": auth_data}


@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    auth_data = AuthService.authenticate_user(db, data.email, data.password)
    return {"data": auth_data}


@router.post("/logout")
def logout():
    return {"data": {"message": "Successfully logged out"}}


@router.get("/me", response_model=DataResponse[UserResponse])
def get_me(current_user: User = Depends(get_current_user)):
    return {"data": UserResponse.model_validate(current_user)}


@router.get("/protected", response_model=DataResponse[dict])
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "data": {
            "message": f"Hello, {current_user.full_name}! You have accessed a protected resource.",
            "user_id": str(current_user.id),
            "role": current_user.role,
        }
    }
