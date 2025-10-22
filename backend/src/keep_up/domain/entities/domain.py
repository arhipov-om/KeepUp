from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Domain:
    """Доменная сущность для отслеживаемого домена"""

    uuid: UUID
    user_uuid: UUID
    url: str
    created_at: datetime

    # def __post_init__(self):
    #     if not self.url.startswith(("http://", "https://")):
    #         self.url = f"https://{self.url}"


@dataclass
class HealthCheck:
    """Доменная сущность для результата проверки"""

    uuid: UUID
    domain_uuid: UUID
    status_code: int | None
    response_time: float
    checked_at: datetime
    error_message: str | None = None

    @property
    def is_available(self) -> bool:
        return self.status_code is not None and 200 <= self.status_code < 400
