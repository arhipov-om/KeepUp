import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta

import uvicorn
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from environs import Env
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from taskiq.api import run_scheduler_task

from keep_up.infrastructure.di import create_container
from keep_up.infrastructure.taskiq.scheduler import get_scheduler
from keep_up.infrastructure.taskiq.tasks import broker
from keep_up.presentation.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    container: AsyncContainer = app.state.dishka_container
    scheduler = get_scheduler(broker=broker, container=container)
    asyncio.create_task(
        run_scheduler_task(
            scheduler,
            run_startup=True,
            interval=timedelta(seconds=5),
        )
    )

    yield
    await container.close()


def create_app() -> FastAPI:
    """Создать и настроить приложение FastAPI"""

    env = Env()
    env.read_env()

    app = FastAPI(
        title="Domain Monitor API",
        description="API для мониторинга доступности доменов",
        version="1.0.0",
        lifespan=lifespan,
        openapi_tags=[
            {
                "name": "users",
                "description": "Operations with users. The **login** logic is also here.",
            },
        ],
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container = create_container(env=env)
    setup_dishka(container, app)
    app.include_router(router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
