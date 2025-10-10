from dishka import AsyncContainer
from dishka.integrations.taskiq import setup_dishka
from taskiq import TaskiqScheduler, AsyncBroker
from taskiq.schedule_sources import LabelScheduleSource


def get_scheduler(broker: AsyncBroker, container: AsyncContainer):
    scheduler = TaskiqScheduler(
        broker=broker,
        sources=[LabelScheduleSource(broker)],
    )
    setup_dishka(container=container, broker=broker)
    return scheduler
