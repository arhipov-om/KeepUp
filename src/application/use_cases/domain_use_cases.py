# src/application/use_cases/domain_use_cases.py
from datetime import datetime, timedelta
from typing import List
from src.domain.entities.domain import Domain, HealthCheck
from src.domain.repositories.domain_repository import DomainRepository, HealthCheckRepository


class AddDomainUseCase:
    """Сценарий добавления домена"""

    def __init__(self, domain_repo: DomainRepository):
        self.domain_repo = domain_repo

    async def execute(self, url: str) -> Domain:
        # Проверяем, существует ли домен
        existing = await self.domain_repo.get_by_url(url)
        if existing:
            raise ValueError(f"Domain {url} already exists")

        domain = Domain(
            id=None,
            url=url,
            created_at=datetime.utcnow()
        )

        return await self.domain_repo.add(domain)


class GetDomainHealthUseCase:
    """Сценарий получения истории проверок домена"""

    def __init__(
            self,
            domain_repo: DomainRepository,
            health_repo: HealthCheckRepository
    ):
        self.domain_repo = domain_repo
        self.health_repo = health_repo

    async def execute(self, domain_id: int, hours: int = 24) -> List[HealthCheck]:
        domain = await self.domain_repo.get_by_id(domain_id)
        if not domain:
            raise ValueError(f"Domain with id {domain_id} not found")

        since = datetime.utcnow() - timedelta(hours=hours)
        return await self.health_repo.get_by_domain(domain_id, since)


class GetAllDomainsUseCase:
    """Сценарий получения всех доменов"""

    def __init__(self, domain_repo: DomainRepository):
        self.domain_repo = domain_repo

    async def execute(self) -> List[Domain]:
        return await self.domain_repo.get_all()