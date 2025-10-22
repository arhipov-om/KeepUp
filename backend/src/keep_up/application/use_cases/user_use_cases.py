import uuid
from datetime import datetime

import bcrypt

from keep_up.domain.entities.user import User
from keep_up.domain.exceptions import UserConflictError
from keep_up.domain.repositories.user_repository import UserRepository


class CreateUserUseCase:
    """Сценарий получения создания пользователя"""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(
        self,
        email: str,
        password: str,
        username: str,
    ) -> User:
        if await self.user_repo.get_by_username(username):
            raise UserConflictError("Username already taken")

        if await self.user_repo.get_by_email(email):
            raise UserConflictError("Email already registered")

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User(
            uuid=uuid.uuid4(),
            username=username,
            email=email,
            password_hash=hashed_password,
            created_at=datetime.now(),
        )
        return await self.user_repo.add(user=user)


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, username: str, password: str) -> User | None:
        if user := (await self.user_repo.get_by_username(username)):
            if bcrypt.checkpw(password.encode(), user.password_hash):
                return user
        return None
