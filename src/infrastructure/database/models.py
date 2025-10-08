# src/infrastructure/database/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class DomainModel(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    health_checks = relationship("HealthCheckModel", back_populates="domain", cascade="all, delete-orphan")


class HealthCheckModel(Base):
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    status_code = Column(Integer, nullable=True)
    response_time = Column(Float, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    error_message = Column(Text, nullable=True)

    domain = relationship("DomainModel", back_populates="health_checks")