# src/infrastructure/database/repositories.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.domain import Domain, HealthCheck
from src.domain.repositories.domain_repository import DomainRepository, HealthCheckRepository
from src.infrastructure.database.models import DomainModel, HealthCheckModel


class SQLAlchemyDomainRepository(DomainRepository):
    """Реализация репозитория доменов через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, domain: Domain) -> Domain:
        model = DomainModel(
            url=domain.url,
            created_at=domain.created_at
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return Domain(
            id=model.id,
            url=model.url,
            created_at=model.created_at
        )

    async def get_by_id(self, domain_id: int) -> Optional[Domain]:
        result = await self.session.execute(
            select(DomainModel).where(DomainModel.id == domain_id)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return Domain(
            id=model.id,
            url=model.url,
            created_at=model.created_at
        )

    async def get_by_url(self, url: str) -> Optional[Domain]:
        result = await self.session.execute(
            select(DomainModel).where(DomainModel.url == url)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return Domain(
            id=model.id,
            url=model.url,
            created_at=model.created_at
        )

    async def get_all(self) -> List[Domain]:
        result = await self.session.execute(select(DomainModel))
        models = result.scalars().all()

        return [
            Domain(
                id=model.id,
                url=model.url,
                created_at=model.created_at
            )
            for model in models
        ]


class SQLAlchemyHealthCheckRepository(HealthCheckRepository):
    """Реализация репозитория проверок через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, health_check: HealthCheck) -> HealthCheck:
        model = HealthCheckModel(
            domain_id=health_check.domain_id,
            status_code=health_check.status_code,
            response_time=health_check.response_time,
            checked_at=health_check.checked_at,
            error_message=health_check.error_message
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return HealthCheck(
            id=model.id,
            domain_id=model.domain_id,
            status_code=model.status_code,
            response_time=model.response_time,
            checked_at=model.checked_at,
            error_message=model.error_message
        )

    async def get_by_domain(
            self,
            domain_id: int,
            since: datetime
    ) -> List[HealthCheck]:
        result = await self.session.execute(
            select(HealthCheckModel)
            .where(
                HealthCheckModel.domain_id == domain_id,
                HealthCheckModel.checked_at >= since
            )
            .order_by(HealthCheckModel.checked_at.desc())
        )
        models = result.scalars().all()

        return [
            HealthCheck(
                id=model.id,
                domain_id=model.domain_id,
                status_code=model.status_code,
                response_time=model.response_time,
                checked_at=model.checked_at,
                error_message=model.error_message
            )
            for model in models
        ]

    async def get_latest_by_domain(self, domain_id: int) -> Optional[HealthCheck]:
        result = await self.session.execute(
            select(HealthCheckModel)
            .where(HealthCheckModel.domain_id == domain_id)
            .order_by(HealthCheckModel.checked_at.desc())
            .limit(1)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return HealthCheck(
            id=model.id,
            domain_id=model.domain_id,
            status_code=model.status_code,
            response_time=model.response_time,
            checked_at=model.checked_at,
            error_message=model.error_message
        )