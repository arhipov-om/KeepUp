# src/infrastructure/scheduler/background_tasks.py
import asyncio
from contextlib import asynccontextmanager

from dishka import AsyncContainer

from keep_up.application.services.health_checker import HealthCheckerService


class BackgroundScheduler:
    """Планировщик фоновых задач"""

    def __init__(self, container: AsyncContainer):
        self.container = container
        self.task = None
        self.running = False

    async def check_domains_periodically(self):
        """Периодическая проверка доменов каждые 5 минут"""
        while self.running:
            try:
                async with self.container() as request_container:
                    service = await request_container.get(HealthCheckerService)
                    await service.check_all_domains()
                    print(f"Health check completed at {asyncio.get_event_loop().time()}")
            except Exception as e:
                print(f"Error during health check: {e}")

            # Ждем 5 минут (300 секунд)
            await asyncio.sleep(300)

    async def start(self):
        """Запустить планировщик"""
        if not self.running:
            self.running = True
            self.task = asyncio.create_task(self.check_domains_periodically())
            print("Background scheduler started")

    async def stop(self):
        """Остановить планировщик"""
        if self.running:
            self.running = False
            if self.task:
                self.task.cancel()
                try:
                    await self.task
                except asyncio.CancelledError:
                    pass
            print("Background scheduler stopped")


@asynccontextmanager
async def lifespan_with_scheduler(app, container: AsyncContainer):
    """Lifespan context manager для FastAPI с планировщиком"""
    scheduler = BackgroundScheduler(container)
    await scheduler.start()

    yield

    await scheduler.stop()
