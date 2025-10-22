from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OkResponse(BaseModel):
    status: int = 200


class RegisterUserRequest(BaseModel):
    email: str
    password: str
    username: str


class LoginUserRequest(BaseModel):
    username: str
    password: str


class RegisterUserResponse(BaseModel):
    uuid: UUID
    email: str
    username: str


class LoginUserResponse(BaseModel):
    uuid: UUID
    username: str
    email: str
    token: str


class AddDomainRequest(BaseModel):
    url: str


class DomainResponse(BaseModel):
    uuid: UUID
    url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HealthCheckResponse(BaseModel):
    uuid: UUID
    domain_uuid: UUID
    status_code: int | None
    response_time: float
    checked_at: datetime
    error_message: str | None
    is_available: bool

    model_config = ConfigDict(from_attributes=True)


class DomainHealthResponse(BaseModel):
    domain: DomainResponse
    checks: list[HealthCheckResponse]


class ErrorResponse(BaseModel):
    detail: str
