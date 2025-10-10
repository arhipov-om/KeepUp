from dataclasses import dataclass

from environs import Env
from pydantic import BaseModel, AmqpDsn, PostgresDsn

# TODO: вынести в env
class TaskiqConfig(BaseModel):
    url: AmqpDsn = AmqpDsn("amqp://guest:guest@localhost:5672//")

class PostgresConfig(BaseModel):
    host: str = "localhost"
    driver: str = "asyncpg"
    port: int = 5555
    user: str = "postgres"
    password: str = "postgres"
    db: str = "keepup"

    url: PostgresDsn  = PostgresDsn(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    url_with_driver: PostgresDsn  = PostgresDsn(f"postgresql+{driver}://{user}:{password}@{host}:{port}/{db}")

@dataclass
class Config:
    taskiq: TaskiqConfig
    db: PostgresConfig


def get_config(env: Env) -> Config:
    return Config(
        taskiq=TaskiqConfig(),
        db=PostgresConfig(
            host=env.str("DB_HOST", default="localhost"),
            driver=env.str("DB_DRIVER", default="asyncpg"),
            port=env.int("DB_PORT", default=5432),
            user=env.str("DB_USER", default="postgres"),
            password=env.str("DB_PASSWORD", default=""),
            db=env.str("DB_NAME", default="keepup"),
        )
    )

taskiq_config = TaskiqConfig()