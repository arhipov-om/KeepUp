import asyncio
import logging
from datetime import datetime

from dishka import FromDishka
from dishka.integrations.taskiq import inject
from environs import env

from keep_up.application.services.health_checker import HealthCheckerService

from keep_up.domain.entities.domain import Domain
from keep_up.domain.repositories.domain_repository import DomainRepository
from keep_up.infrastructure.config import get_message_queue_config
from keep_up.infrastructure.taskiq.config import create_broker

logger = logging.getLogger(__name__)
env.read_env()

broker = create_broker(
    message_queue=get_message_queue_config(env=env).url.unicode_string(),
    max_async_tasks=100,
)


@broker.task(
    task_name="check_single_domain",
    retry_on_error=True,
    max_retries=3,
    retry_delay=10.0,
)
@inject(patch_module=True)
async def check_single_domain_task(
    domain: Domain,
    service: FromDishka[HealthCheckerService],
) -> None:
    try:
        result = await service.check_domain(domain)
        print(result)
    except Exception:
        raise


@broker.task(
    schedule=[{"cron": "*/1 * * * *"}],
    task_name="schedule_domain_checks",
)
@inject(patch_module=True)
async def schedule_domain_checks_task(
    domain_repo: FromDishka[DomainRepository],
) -> None:
    """
    Планировщик: каждые 5 минут берёт все домены и ставит задачу на проверку.
    """
    start_time = datetime.now()
    logger.info("Starting domain check scheduling")

    domains = await domain_repo.get_all()
    total = len(domains)
    domains = domains * 100

    if total == 0:
        logger.info("No active domains to check")
        return

    logger.info("Found domains to check, %s", total)

    batch_size = 50
    scheduled = 0

    for i in range(0, total, batch_size):
        batch = domains[i : i + batch_size]

        tasks = [check_single_domain_task.kiq(domain=domain) for domain in batch]
        await asyncio.gather(*tasks, return_exceptions=True)
        scheduled += len(batch)

        if scheduled % 500 == 0:
            logger.info("Scheduled batch, %s %s", scheduled, total)

    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info("Scheduling completed  %s %s %s", scheduled, total, elapsed)
