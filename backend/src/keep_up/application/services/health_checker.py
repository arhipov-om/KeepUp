# src/application/services/health_checker.py
import asyncio
from datetime import datetime
from typing import Optional

import aiohttp
import httpx
from httpx import AsyncClient

from keep_up.domain.entities.domain import Domain, HealthCheck
from keep_up.domain.repositories.domain_repository import DomainRepository, HealthCheckRepository

session = AsyncClient()

class HealthCheckerService:
    """Сервис для проверки доступности доменов"""

    def __init__(
            self,
            domain_repo: DomainRepository,
            health_repo: HealthCheckRepository
    ):
        self.domain_repo = domain_repo
        self.health_repo = health_repo

    async def check_domain(self, domain: Domain) -> HealthCheck:
        """Проверить один домен"""
        start_time = datetime.now()
        status_code: Optional[int] = None
        error_message: Optional[str] = None

        try:
            response = await session.get(
                        domain.url,
                        timeout=10,
                        follow_redirects=True
                )
            status_code = response.status_code
        except httpx.ReadError as e:
            error_message = str(e)
        except httpx.TimeoutException:
            error_message = "Request timeout"
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"

        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000

        health_check = HealthCheck(
            id=None,
            domain_id=domain.id,
            status_code=status_code,
            response_time=response_time,
            checked_at=datetime.now(),
            error_message=error_message
        )

        return await self.health_repo.add(health_check)
