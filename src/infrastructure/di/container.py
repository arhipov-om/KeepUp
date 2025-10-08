# src/infrastructure/di/container.py
from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.domain.repositories.domain_repository import DomainRepository, HealthCheckRepository
from src.infrastructure.database.repositories import SQLAlchemyDomainRepository, SQLAlchemyHealthCheckRepository
from src.application.use_cases.domain_use_cases import AddDomainUseCase, GetDomainHealthUseCase, GetAllDomainsUseCase
from src.application.services.health_checker import HealthCheckerService


class DatabaseProvider(Provider):
    """Provider для работы с базой данных"""

    @provide(scope=Scope.APP)
    def get_engine(self) -> create_async_engine:
        return create_async_engine(
            "sqlite+aiosqlite:///./domain_monitor.db",
            echo=False
        )

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, engine: create_async_engine) -> async_sessionmaker:
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(self, sessionmaker: async_sessionmaker) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session


class RepositoryProvider(Provider):
    """Provider для репозиториев"""

    @provide(scope=Scope.REQUEST)
    def get_domain_repository(self, session: AsyncSession) -> DomainRepository:
        return SQLAlchemyDomainRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_health_check_repository(self, session: AsyncSession) -> HealthCheckRepository:
        return SQLAlchemyHealthCheckRepository(session)


class UseCaseProvider(Provider):
    """Provider для use cases"""

    @provide(scope=Scope.REQUEST)
    def get_add_domain_use_case(
            self,
            domain_repo: DomainRepository
    ) -> AddDomainUseCase:
        return AddDomainUseCase(domain_repo)

    @provide(scope=Scope.REQUEST)
    def get_domain_health_use_case(
            self,
            domain_repo: DomainRepository,
            health_repo: HealthCheckRepository
    ) -> GetDomainHealthUseCase:
        return GetDomainHealthUseCase(domain_repo, health_repo)

    @provide(scope=Scope.REQUEST)
    def get_all_domains_use_case(
            self,
            domain_repo: DomainRepository
    ) -> GetAllDomainsUseCase:
        return GetAllDomainsUseCase(domain_repo)


class ServiceProvider(Provider):
    """Provider для сервисов"""

    @provide(scope=Scope.REQUEST)
    def get_health_checker_service(
            self,
            domain_repo: DomainRepository,
            health_repo: HealthCheckRepository
    ) -> HealthCheckerService:
        return HealthCheckerService(domain_repo, health_repo)