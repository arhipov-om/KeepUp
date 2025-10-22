from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    """Доменная сущность пользователя"""

    uuid: UUID
    username: str
    email: str
    password_hash: bytes
    created_at: datetime
