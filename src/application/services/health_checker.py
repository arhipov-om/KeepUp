# src/application/services/health_checker.py
import asyncio
import aiohttp
from datetime import datetime
from typing import Optional
from src.domain.entities.domain import Domain, HealthCheck
from src.domain.repositories.domain_repository import DomainRepository, HealthCheckRepository


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
        start_time = datetime.utcnow()
        status_code: Optional[int] = None
        error_message: Optional[str] = None

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        domain.url,
                        timeout=aiohttp.ClientTimeout(total=10),
                        allow_redirects=True
                ) as response:
                    status_code = response.status
        except aiohttp.ClientError as e:
            error_message = str(e)
        except asyncio.TimeoutError:
            error_message = "Request timeout"
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"

        end_time = datetime.utcnow()
        response_time = (end_time - start_time).total_seconds() * 1000

        health_check = HealthCheck(
            id=None,
            domain_id=domain.id,
            status_code=status_code,
            response_time=response_time,
            checked_at=datetime.utcnow(),
            error_message=error_message
        )

        return await self.health_repo.add(health_check)

    async def check_all_domains(self):
        """Проверить все домены"""
        domains = await self.domain_repo.get_all()

        tasks = [self.check_domain(domain) for domain in domains]
        await asyncio.gather(*tasks, return_exceptions=True)