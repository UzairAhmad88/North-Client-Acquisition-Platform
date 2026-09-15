"""Communication Policy ORM model."""

from typing import List
from sqlalchemy import JSON, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class CommunicationPolicy(BaseModel):
    """Stores configurable rate limits, daily contact caps, and cooldown policies."""

    __tablename__ = "communication_policies"

    name: Mapped[str] = mapped_column(String(64), nullable=False, default="DEFAULT_POLICY", unique=True)
    max_per_contact_per_day: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    max_per_business_per_day: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    cooldown_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=24)
    allowed_channels: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=lambda: ["EMAIL", "WHATSAPP", "SMS", "LINKEDIN"])
    require_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
