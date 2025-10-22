from abc import ABC, abstractmethod
from uuid import UUID

from keep_up.domain.entities.user import User


class UserRepository(ABC):
    """Интерфейс репозитория для доменов"""

    @abstractmethod
    async def add(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_uuid(self, user_uuid: UUID) -> User | None:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[User]:
        pass
