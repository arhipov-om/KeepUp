# src/presentation/api/schemas.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl


class AddDomainRequest(BaseModel):
    url: str


class DomainResponse(BaseModel):
    id: int
    url: str
    created_at: datetime

    class Config:
        from_attributes = True


class HealthCheckResponse(BaseModel):
    id: int
    domain_id: int
    status_code: Optional[int]
    response_time: float
    checked_at: datetime
    error_message: Optional[str]
    is_available: bool

    class Config:
        from_attributes = True


class DomainHealthResponse(BaseModel):
    domain: DomainResponse
    checks: List[HealthCheckResponse]


class ErrorResponse(BaseModel):
    detail: str