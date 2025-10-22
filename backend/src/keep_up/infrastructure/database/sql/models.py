import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .core import Base
from .mixins import TimestampMixin, UUIDMixin


class UserORM(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password_hash: Mapped[bytes]

    domains: Mapped[list["DomainORM"]] = relationship(
        "DomainORM",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class DomainORM(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "domains"
    __table_args__ = (UniqueConstraint("url", "user_uuid"),)

    url: Mapped[str] = mapped_column(String(254), nullable=False)
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), nullable=False)

    user: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="domains",
    )
    health_checks: Mapped[list["HealthCheckORM"]] = relationship(
        "HealthCheckORM",
        back_populates="domain",
        cascade="all, delete-orphan",
    )


class HealthCheckORM(Base, UUIDMixin):
    __tablename__ = "health_checks"

    domain_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("domains.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status_code: Mapped[int | None]
    response_time: Mapped[float]
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    error_message: Mapped[str | None]

    domain: Mapped["DomainORM"] = relationship(
        "DomainORM",
        back_populates="health_checks",
    )
