from typing import AsyncIterable

from dishka import Provider, Scope, provide, from_context
from environs import Env
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from keep_up.infrastructure.config import get_config, Config

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


class DatabaseProvider(Provider):
    """Provider для работы с базой данных"""

    scope = Scope.APP

    env = from_context(provides=Env)

    @provide(scope=Scope.APP)
    def get_config(self, env: Env) -> Config:
        return get_config(env=env)

    @provide(scope=Scope.APP)
    def get_engine(self, config: Config) -> create_async_engine:
        return create_async_engine(
            config.db.url_with_driver.unicode_string(),
            echo=False,
        )

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, engine: create_async_engine) -> async_sessionmaker:
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        sessionmaker: async_sessionmaker,
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session
