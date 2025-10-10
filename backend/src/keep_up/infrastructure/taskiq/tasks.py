from datetime import datetime

from dishka import FromDishka
from dishka.integrations.taskiq import inject

from keep_up.application.services.health_checker import HealthCheckerService

from keep_up.domain.entities.domain import Domain
from keep_up.domain.repositories.domain_repository import DomainRepository
from keep_up.infrastructure.config import taskiq_config
from keep_up.infrastructure.taskiq.config import create_broker

broker = create_broker(
    rabbit_url=taskiq_config.url.unicode_string(),
    max_async_tasks=100
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
        domain_repo: FromDishka[DomainRepository],
        service: FromDishka[HealthCheckerService],
) -> None:
    health_check = await service.check_domain(domain)
    print(health_check)


@broker.task(
    schedule=[{"cron": "*/1 * * * *"}],
    task_name="schedule_domain_checks"
)
@inject(patch_module=True)
async def schedule_domain_checks_task(
        domain_repo: FromDishka[DomainRepository],
) -> None:
    """
    Создает отдельную задачу для каждого домена
    Оптимизировано для большого количества доменов (1000+)
    """
    start_time = datetime.now()

    domains = await domain_repo.get_all()
    # domains *= 100
    total_domains = len(domains)
    print(f"[{start_time}] Scheduling checks for {total_domains} domains")

    # Отправляем задачи пакетами для эффективности
    batch_size = 100
    scheduled_count = 0

    for i in range(0, total_domains, batch_size):
        batch = domains[i:i + batch_size]

        # Создаем задачи для батча
        for domain in batch:
            await check_single_domain_task.kiq(domain=domain)
            scheduled_count += 1

        # Логируем прогресс
        if (i + batch_size) % 500 == 0:
            print(f"  Scheduled {scheduled_count}/{total_domains} domains...")

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"[{datetime.now()}] Completed scheduling {scheduled_count} domains in {elapsed:.2f}s")
