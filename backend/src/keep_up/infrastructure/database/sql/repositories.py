from datetime import datetime
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from keep_up.domain.entities.domain import Domain, HealthCheck
from keep_up.domain.entities.user import User
from keep_up.domain.repositories.domain_repository import (
    DomainRepository,
    HealthCheckRepository,
)
from keep_up.domain.repositories.user_repository import UserRepository
from keep_up.infrastructure.database.sql.models import (
    DomainORM,
    HealthCheckORM,
    UserORM,
)


class SQLAlchemyDomainRepository(DomainRepository):
    """Реализация репозитория доменов через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, domain: Domain) -> Domain:
        model = DomainORM(
            uuid=domain.uuid,
            user_uuid=domain.user_uuid,
            url=domain.url,
            created_at=domain.created_at,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return Domain(
            user_uuid=model.user_uuid,
            uuid=model.uuid,
            url=model.url,
            created_at=model.created_at,
        )

    async def get_by_uuid(self, domain_uuid: UUID) -> Domain | None:
        result = await self.session.execute(
            select(DomainORM).where(DomainORM.uuid == domain_uuid)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return Domain(
            user_uuid=model.user_uuid,
            uuid=model.uuid,
            url=model.url,
            created_at=model.created_at,
        )

    async def get_by_url(self, url: str) -> Domain | None:
        result = await self.session.execute(
            select(DomainORM).where(DomainORM.url == url)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return Domain(
            user_uuid=model.user_uuid,
            uuid=model.uuid,
            url=model.url,
            created_at=model.created_at,
        )

    async def get_by_url_uuid_qc(self, url: str, user_uuid: UUID) -> Domain | None:
        result = await self.session.execute(
            select(DomainORM).where(
                DomainORM.url == url,
                DomainORM.user_uuid == user_uuid,
            )
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return Domain(
            user_uuid=model.user_uuid,
            uuid=model.uuid,
            url=model.url,
            created_at=model.created_at,
        )

    async def get_all(self) -> list[Domain]:
        result = await self.session.execute(select(DomainORM))
        models = result.scalars().all()

        return [
            Domain(
                user_uuid=model.user_uuid,
                uuid=model.uuid,
                url=model.url,
                created_at=model.created_at,
            )
            for model in models
        ]


class SQLAlchemyHealthCheckRepository(HealthCheckRepository):
    """Реализация репозитория проверок через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, health_check: HealthCheck) -> HealthCheck:
        model = HealthCheckORM(
            uuid=health_check.uuid,
            domain_uuid=health_check.domain_uuid,
            status_code=health_check.status_code,
            response_time=health_check.response_time,
            checked_at=health_check.checked_at,
            error_message=health_check.error_message,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return HealthCheck(
            uuid=model.uuid,
            domain_uuid=model.domain_uuid,
            status_code=model.status_code,
            response_time=model.response_time,
            checked_at=model.checked_at,
            error_message=model.error_message,
        )

    async def get_by_domain(
        self, domain_uuid: UUID, since: datetime
    ) -> list[HealthCheck]:
        result = await self.session.execute(
            select(HealthCheckORM)
            .where(
                HealthCheckORM.domain_uuid == domain_uuid,
                HealthCheckORM.checked_at >= since,
            )
            .order_by(HealthCheckORM.checked_at.desc())
        )
        models = result.scalars().all()

        return [
            HealthCheck(
                uuid=model.uuid,
                domain_uuid=model.domain_uuid,
                status_code=model.status_code,
                response_time=model.response_time,
                checked_at=model.checked_at,
                error_message=model.error_message,
            )
            for model in models
        ]

    async def get_latest_by_domain(self, domain_uuid: UUID) -> HealthCheck | None:
        result = await self.session.execute(
            select(HealthCheckORM)
            .where(HealthCheckORM.domain_uuid == domain_uuid)
            .order_by(HealthCheckORM.checked_at.desc())
            .limit(1)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return HealthCheck(
            uuid=model.uuid,
            domain_uuid=model.domain_uuid,
            status_code=model.status_code,
            response_time=model.response_time,
            checked_at=model.checked_at,
            error_message=model.error_message,
        )


class SQLAlchemyUserRepository(UserRepository):
    """Реализация репозитория пользователей через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> User:
        model = UserORM(
            uuid=user.uuid,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            password_hash=user.password_hash,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return User(
            uuid=model.uuid,
            username=model.username,
            email=model.email,
            created_at=model.created_at,
            password_hash=model.password_hash,
        )

    async def get_by_uuid(self, user_uuid: UUID) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.uuid == user_uuid)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        return User(
            uuid=model.uuid,
            username=model.username,
            email=model.email,
            created_at=model.created_at,
            password_hash=model.password_hash,
        )

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.username == username)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        return User(
            uuid=model.uuid,
            username=model.username,
            email=model.email,
            created_at=model.created_at,
            password_hash=model.password_hash,
        )

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.email == email)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        return User(
            uuid=model.uuid,
            username=model.username,
            email=model.email,
            created_at=model.created_at,
            password_hash=model.password_hash,
        )

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(UserORM))
        models = result.scalars().all()

        return [
            User(
                uuid=model.uuid,
                username=model.username,
                email=model.email,
                created_at=model.created_at,
                password_hash=model.password_hash,
            )
            for model in models
        ]
