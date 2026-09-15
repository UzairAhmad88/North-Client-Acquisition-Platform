import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import AppError, ForbiddenError, UnauthorizedError
from app.core.security import (
    create_access_token,
    hash_password,
    normalize_email,
    verify_password,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import (
    AuthResponseData,
    AuthToken,
    RegisterRequest,
    UserResponse,
)


class AuthService:
    @staticmethod
    def register_user(db: Session, data: RegisterRequest) -> AuthResponseData:
        normalized = normalize_email(data.email)
        existing = UserRepository.get_by_email(db, normalized)
        if existing:
            raise AppError(
                code="DUPLICATE_ACCOUNT",
                message="An account with this email address already exists",
                status_code=400,
            )

        hashed = hash_password(data.password)
        user = UserRepository.create(
            db=db,
            email=normalized,
            password_hash=hashed,
            full_name=data.full_name,
        )

        token_str = create_access_token({"sub": str(user.id), "role": user.role})
        token = AuthToken(access_token=token_str, expires_in=86400)
        return AuthResponseData(user=UserResponse.model_validate(user), token=token)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> AuthResponseData:
        normalized = normalize_email(email)
        user = UserRepository.get_by_email(db, normalized)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        if not user.is_active:
            raise ForbiddenError("Account is inactive")

        UserRepository.update_last_login(db, user.id)

        token_str = create_access_token({"sub": str(user.id), "role": user.role})
        token = AuthToken(access_token=token_str, expires_in=86400)
        return AuthResponseData(user=UserResponse.model_validate(user), token=token)

    @staticmethod
    def get_user_from_token(db: Session, payload: dict) -> User:
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise UnauthorizedError("Invalid token payload")

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise UnauthorizedError("Invalid token user ID")

        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise UnauthorizedError("User no longer exists")

        if not user.is_active:
            raise ForbiddenError("Account is inactive")

        return user
