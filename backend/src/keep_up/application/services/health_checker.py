import uuid
from datetime import datetime

import httpx
from pytz import UTC

from keep_up.domain.entities.domain import Domain, HealthCheck
from keep_up.domain.repositories.domain_repository import HealthCheckRepository


class HealthCheckerService:
    """Сервис для проверки доступности доменов"""

    def __init__(
        self,
        client: httpx.AsyncClient,
        health_repo: HealthCheckRepository,
    ):
        self.client = client
        self.health_repo: HealthCheckRepository = health_repo

    async def check_domain(
        self,
        domain: Domain,
    ) -> HealthCheck:
        """Проверить один домен"""
        start_time = datetime.now(tz=UTC)
        status_code: int | None = None
        error_message: str | None = None

        try:
            response = await self.client.get(
                domain.url,
                timeout=10,
                follow_redirects=True,
            )
            status_code = response.status_code
        except httpx.ReadError as e:
            error_message = str(e)
        except httpx.TimeoutException:
            error_message = "Request timeout"
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"

        end_time = datetime.now(tz=UTC)
        response_time = (end_time - start_time).total_seconds() * 1000

        health_check = HealthCheck(
            uuid=uuid.uuid4(),
            domain_uuid=domain.uuid,
            status_code=status_code,
            response_time=response_time,
            checked_at=datetime.now(),
            error_message=error_message,
        )
        # return health_check
        return await self.health_repo.add(health_check)
