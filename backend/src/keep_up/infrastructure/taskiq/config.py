from taskiq import AsyncBroker
from taskiq_aio_pika import AioPikaBroker


def create_broker(
    message_queue: str,
    max_async_tasks: int = 100,
) -> AsyncBroker:
    broker = AioPikaBroker(
        message_queue,
        max_connection_pool_size=max_async_tasks,
    )
    return broker
