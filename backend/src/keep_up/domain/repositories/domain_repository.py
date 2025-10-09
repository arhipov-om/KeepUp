# src/domain/repositories/domain_repository.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from keep_up.domain.entities.domain import Domain, HealthCheck


class DomainRepository(ABC):
    """Интерфейс репозитория для доменов"""

    @abstractmethod
    async def add(self, domain: Domain) -> Domain:
        pass

    @abstractmethod
    async def get_by_id(self, domain_id: int) -> Optional[Domain]:
        pass

    @abstractmethod
    async def get_by_url(self, url: str) -> Optional[Domain]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Domain]:
        pass


class HealthCheckRepository(ABC):
    """Интерфейс репозитория для проверок здоровья"""

    @abstractmethod
    async def add(self, health_check: HealthCheck) -> HealthCheck:
        pass

    @abstractmethod
    async def get_by_domain(
            self,
            domain_id: int,
            since: datetime
    ) -> List[HealthCheck]:
        pass

    @abstractmethod
    async def get_latest_by_domain(self, domain_id: int) -> Optional[HealthCheck]:
        pass
