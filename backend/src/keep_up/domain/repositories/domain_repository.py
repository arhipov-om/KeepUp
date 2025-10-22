from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from keep_up.domain.entities.domain import Domain, HealthCheck


class DomainRepository(ABC):
    """Интерфейс репозитория для доменов"""

    @abstractmethod
    async def add(self, domain: Domain) -> Domain:
        pass

    @abstractmethod
    async def get_by_uuid(self, domain_uuid: UUID) -> Domain | None:
        pass

    @abstractmethod
    async def get_by_url(self, url: str) -> Domain | None:
        pass

    @abstractmethod
    async def get_by_url_uuid_qc(self, url: str, user_uuid: UUID) -> Domain | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Domain]:
        pass


class HealthCheckRepository(ABC):
    """Интерфейс репозитория для проверок здоровья"""

    @abstractmethod
    async def add(self, health_check: HealthCheck) -> HealthCheck:
        pass

    @abstractmethod
    async def get_by_domain(
        self,
        domain_uuid: UUID,
        since: datetime,
    ) -> list[HealthCheck]:
        pass

    @abstractmethod
    async def get_latest_by_domain(self, domain_uuid: UUID) -> HealthCheck | None:
        pass
