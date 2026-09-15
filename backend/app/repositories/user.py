import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(
        db: Session,
        email: str,
        password_hash: str,
        full_name: str,
        role: str = "MEMBER",
    ) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role=role,
            is_active=True,
            is_verified=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_last_login(db: Session, user_id: uuid.UUID) -> None:
        user = UserRepository.get_by_id(db, user_id)
        if user:
            user.last_login_at = datetime.now(timezone.utc)
            db.commit()

    @staticmethod
    def set_active(db: Session, user_id: uuid.UUID, is_active: bool) -> Optional[User]:
        user = UserRepository.get_by_id(db, user_id)
        if user:
            user.is_active = is_active
            db.commit()
            db.refresh(user)
        return user
