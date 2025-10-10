# main.py
import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta

import uvicorn
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.taskiq import setup_dishka as taskiq_setup_dishka
from environs import Env
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from taskiq import AsyncBroker
from taskiq.api import run_scheduler_task

from keep_up.infrastructure.database.sql.models import Base
from keep_up.infrastructure.di import (
    DatabaseProvider,
    RepositoryProvider,
    UseCaseProvider,
    ServiceProvider
)
from keep_up.infrastructure.taskiq.scheduler import get_scheduler
from keep_up.infrastructure.taskiq.tasks import broker
from keep_up.presentation.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Создаем таблицы БД
    container: AsyncContainer = app.state.dishka_container

    engine = await container.get(create_async_engine)

    scheduler = get_scheduler(broker=broker, container=container)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    asyncio.create_task(run_scheduler_task(scheduler, run_startup=True, interval=timedelta(seconds=1)))

    yield
    await container.close()
    await engine.dispose()


def create_app() -> FastAPI:
    """Создать и настроить приложение FastAPI"""

    env = Env()
    env.read_env()

    app = FastAPI(
        title="Domain Monitor API",
        description="API для мониторинга доступности доменов",
        version="1.0.0",
        lifespan=lifespan
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Настройка DI контейнера
    container = make_async_container(
        DatabaseProvider(),
        RepositoryProvider(),
        UseCaseProvider(),
        ServiceProvider(),
        context={Env: env}
    )
    setup_dishka(container, app)

    # Подключение роутов
    app.include_router(router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
