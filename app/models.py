import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class EnvType(str, enum.Enum):
    prod = "prod"
    preprod = "preprod"
    stage = "stage"


class DomainType(str, enum.Enum):
    canary = "canary"
    regular = "regular"


class User(Base):
    """Основная модель базы данных"""
    
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    project_id: Mapped[uuid.UUID]
    env: Mapped[EnvType] = mapped_column(Enum(EnvType))
    domain: Mapped[DomainType] = mapped_column(Enum(DomainType))
    locktime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

