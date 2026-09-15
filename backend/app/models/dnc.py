"""Do-Not-Contact (DNC) Registry ORM model."""

import uuid
from typing import Optional
from sqlalchemy import Boolean, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class DoNotContact(BaseModel):
    """Stores Do-Not-Contact registry entries to prevent accidental communications."""

    __tablename__ = "do_not_contact"

    scope: Mapped[str] = mapped_column(String(32), nullable=False, default="EMAIL", index=True)  # EMAIL, PHONE, CONTACT, BUSINESS, GLOBAL
    target_value: Mapped[str] = mapped_column(String(255), nullable=False, index=True)  # Normalized email, phone, or UUID
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
