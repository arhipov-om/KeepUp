from dataclasses import dataclass

from environs import Env
from pydantic import BaseModel, AmqpDsn, PostgresDsn


class TaskiqConfig(BaseModel):
    url: AmqpDsn = AmqpDsn("amqp://guest:guest@localhost:5672//")


class PostgresConfig(BaseModel):
    host: str
    driver: str
    port: int
    user: str
    password: str
    db: str

    @property
    def url(self):
        return PostgresDsn(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )

    @property
    def url_with_driver(self):
        return PostgresDsn(
            f"postgresql+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )


@dataclass
class Config:
    message_queue: TaskiqConfig
    db: PostgresConfig


def get_database_config(env: Env) -> PostgresConfig:
    return PostgresConfig(
        host=env.str("DB_HOST"),
        driver=env.str("DB_DRIVER"),
        port=env.int("DB_PORT"),
        user=env.str("DB_USER"),
        password=env.str("DB_PASS"),
        db=env.str("DB_NAME", default="keepup"),
    )


def get_message_queue_config(env: Env):
    return TaskiqConfig(
        url=AmqpDsn(env.str("BROKER_URL")),
    )


def get_config(env: Env) -> Config:
    return Config(
        message_queue=get_message_queue_config(env=env),
        db=get_database_config(env=env),
    )
