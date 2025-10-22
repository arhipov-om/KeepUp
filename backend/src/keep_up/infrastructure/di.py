from dishka import Provider, Scope, provide, make_async_container
from environs import Env
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from keep_up.application.services.health_checker import HealthCheckerService
from keep_up.application.services.user_service import UserService
from keep_up.application.use_cases.domain_use_cases import (
    AddDomainUseCase,
    GetDomainHealthUseCase,
    GetAllDomainsUseCase,
)
from keep_up.domain.repositories.domain_repository import (
    DomainRepository,
    HealthCheckRepository,
)
from keep_up.domain.repositories.user_repository import UserRepository
from keep_up.infrastructure.database.sql.core import DatabaseProvider
from keep_up.infrastructure.database.sql.repositories import (
    SQLAlchemyDomainRepository,
    SQLAlchemyHealthCheckRepository,
    SQLAlchemyUserRepository,
)


class RepositoryProvider(Provider):
    """Provider для репозиториев"""

    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return SQLAlchemyUserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_domain_repository(self, session: AsyncSession) -> DomainRepository:
        return SQLAlchemyDomainRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_health_check_repository(
        self, session: AsyncSession
    ) -> HealthCheckRepository:
        return SQLAlchemyHealthCheckRepository(session)


class UseCaseProvider(Provider):
    """Provider для use cases"""

    @provide(scope=Scope.REQUEST)
    def get_add_domain_use_case(
        self,
        domain_repo: DomainRepository,
    ) -> AddDomainUseCase:
        return AddDomainUseCase(domain_repo)

    @provide(scope=Scope.REQUEST)
    def get_domain_health_use_case(
        self,
        domain_repo: DomainRepository,
        health_repo: HealthCheckRepository,
    ) -> GetDomainHealthUseCase:
        return GetDomainHealthUseCase(domain_repo, health_repo)

    @provide(scope=Scope.REQUEST)
    def get_all_domains_use_case(
        self,
        domain_repo: DomainRepository,
    ) -> GetAllDomainsUseCase:
        return GetAllDomainsUseCase(domain_repo)


class ServiceProvider(Provider):
    """Provider для сервисов"""

    @provide(scope=Scope.APP)
    async def get_client(self) -> AsyncClient:
        return AsyncClient()
        # client = AsyncClient()
        # yield client
        # await client.aclose()

    @provide(scope=Scope.REQUEST)
    def get_health_checker_service(
        self,
        client: AsyncClient,
        health_repo: HealthCheckRepository,
    ) -> HealthCheckerService:
        return HealthCheckerService(client=client, health_repo=health_repo)

    @provide(scope=Scope.REQUEST)
    def get_user_service(
        self,
        user_repo: UserRepository,
    ) -> UserService:
        return UserService(user_repo=user_repo)


def create_container(env: Env):
    return make_async_container(
        DatabaseProvider(),
        RepositoryProvider(),
        UseCaseProvider(),
        ServiceProvider(),
        context={Env: env},
    )
