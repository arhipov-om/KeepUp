import logging
from uuid import UUID

from keep_up.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    LoginUserUseCase,
)
from keep_up.domain.entities.user import User
from keep_up.domain.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
    ):
        self.user_repo = user_repo
        self.create_user_use_case = CreateUserUseCase(self.user_repo)
        self.login_user_use_case = LoginUserUseCase(self.user_repo)

    async def register_user(
        self,
        username: str,
        email: str,
        password: str,
    ):
        logger.debug(f"Registering user username=%s", username)
        user = await self.create_user_use_case.execute(
            username=username, email=email, password=password
        )
        return user

    async def login_user(
        self,
        username: str,
        password: str,
    ) -> User | None:
        return await self.login_user_use_case.execute(
            username=username,
            password=password,
        )

    async def get_user(
        self,
        user_uuid: UUID,
    ) -> User | None:
        return await self.user_repo.get_by_uuid(user_uuid=user_uuid)

    async def get_user_by_username(
        self,
        username: str,
    ) -> User | None:
        return await self.user_repo.get_by_username(username=username)
