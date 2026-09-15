from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class SystemLog(BaseModel):
    __tablename__ = "system_logs"

    level: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    component: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
