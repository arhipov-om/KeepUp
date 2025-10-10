from taskiq import AsyncBroker
from taskiq_aio_pika import AioPikaBroker


def create_broker(
        rabbit_url: str,
        max_async_tasks: int = 100
) -> AsyncBroker:
    broker = AioPikaBroker(
        rabbit_url,
        max_connection_pool_size=max_async_tasks
    )
    return broker
