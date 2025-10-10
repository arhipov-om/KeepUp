import asyncio
from multiprocessing import Process

from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka
from environs import Env
from taskiq.api import run_receiver_task

from keep_up.infrastructure.di import ServiceProvider, UseCaseProvider, RepositoryProvider, DatabaseProvider
from keep_up.infrastructure.taskiq.tasks import broker


async def start_worker():
    """
    Запуск одного воркера с локальным контейнером DI
    """

    env = Env()
    env.read_env()

    container = make_async_container(
        DatabaseProvider(),
        RepositoryProvider(),
        UseCaseProvider(),
        ServiceProvider(),
        context={Env: env}
    )
    setup_dishka(container=container, broker=broker)
    print('yoyo')
    await run_receiver_task(broker, run_startup=True)


def run_worker_process():
    """
    Обёртка для запуска воркера в отдельном процессе
    """
    asyncio.run(start_worker())


if __name__ == '__main__':
    num_workers = 4
    processes = []

    for _ in range(num_workers):
        p = Process(target=run_worker_process)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
