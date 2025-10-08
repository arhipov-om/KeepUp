# src/domain/entities/domain.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Domain:
    """Доменная сущность для отслеживаемого домена"""
    id: Optional[int]
    url: str
    created_at: datetime

    def __post_init__(self):
        if not self.url.startswith(('http://', 'https://')):
            self.url = f'https://{self.url}'


@dataclass
class HealthCheck:
    """Доменная сущность для результата проверки"""
    id: Optional[int]
    domain_id: int
    status_code: Optional[int]
    response_time: float  # в миллисекундах
    checked_at: datetime
    error_message: Optional[str] = None

    @property
    def is_available(self) -> bool:
        return self.status_code is not None and 200 <= self.status_code < 400