import uuid
from datetime import datetime, timedelta
from uuid import UUID

from keep_up.domain.entities.domain import Domain, HealthCheck
from keep_up.domain.exceptions import DomainAlreadyExistsError
from keep_up.domain.repositories.domain_repository import (
    DomainRepository,
    HealthCheckRepository,
)


class AddDomainUseCase:
    """Сценарий добавления домена"""

    def __init__(
        self,
        domain_repo: DomainRepository,
    ):
        self.domain_repo = domain_repo

    async def execute(
        self,
        user_uuid: UUID,
        url: str,
    ) -> Domain:
        existing = await self.domain_repo.get_by_url_uuid_qc(
            url=url, user_uuid=user_uuid
        )
        if existing:
            raise DomainAlreadyExistsError(f"Domain {url} already exists")

        domain = Domain(
            user_uuid=user_uuid,
            uuid=uuid.uuid4(),
            url=url,
            created_at=datetime.now(),
        )

        return await self.domain_repo.add(domain)


class GetDomainHealthUseCase:
    """Сценарий получения истории проверок домена"""

    def __init__(
        self,
        domain_repo: DomainRepository,
        health_repo: HealthCheckRepository,
    ):
        self.domain_repo = domain_repo
        self.health_repo = health_repo

    async def execute(self, domain_uuid: UUID, hours: int = 24) -> list[HealthCheck]:
        domain = await self.domain_repo.get_by_uuid(domain_uuid)
        if not domain:
            raise ValueError(f"Domain with id {domain_uuid} not found")

        since = datetime.now() - timedelta(hours=hours)
        return await self.health_repo.get_by_domain(domain_uuid, since)


class GetAllDomainsUseCase:
    """Сценарий получения всех доменов"""

    def __init__(
        self,
        domain_repo: DomainRepository,
    ):
        self.domain_repo = domain_repo

    async def execute(self) -> list[Domain]:
        return await self.domain_repo.get_all()
