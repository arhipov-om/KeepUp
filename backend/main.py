# main.py
from contextlib import asynccontextmanager

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine

from keep_up.infrastructure.database.sql.models import Base
from keep_up.infrastructure.di import (
    DatabaseProvider,
    RepositoryProvider,
    UseCaseProvider,
    ServiceProvider
)
from keep_up.infrastructure.scheduler.background_tasks import BackgroundScheduler
from keep_up.presentation.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Создаем таблицы БД
    engine = create_async_engine("sqlite+aiosqlite:///./domain_monitor.db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Запускаем планировщик
    scheduler = BackgroundScheduler(app.state.dishka_container)
    await scheduler.start()

    yield

    await app.state.dishka_container.close()
    # Останавливаем планировщик
    await scheduler.stop()
    await engine.dispose()


def create_app() -> FastAPI:
    """Создать и настроить приложение FastAPI"""
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
        ServiceProvider()
    )
    setup_dishka(container, app)

    # Подключение роутов
    app.include_router(router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
