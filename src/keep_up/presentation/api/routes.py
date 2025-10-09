# src/presentation/api/routes.py
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, HTTPException

from keep_up.application.use_cases.domain_use_cases import (
    AddDomainUseCase,
    GetDomainHealthUseCase,
    GetAllDomainsUseCase
)
from keep_up.presentation.api.schemas import (
    AddDomainRequest,
    DomainResponse,
    HealthCheckResponse
)

router = APIRouter(prefix="/api", tags=["domains"], route_class=DishkaRoute)


@router.post("/domains", response_model=DomainResponse, status_code=201)
async def add_domain(
        request: AddDomainRequest,
        use_case: FromDishka[AddDomainUseCase]
):
    """Добавить новый домен для мониторинга"""
    try:
        domain = await use_case.execute(request.url)
        return DomainResponse(
            id=domain.id,
            url=domain.url,
            created_at=domain.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/domains", response_model=list[DomainResponse])
async def get_all_domains(
        use_case: FromDishka[GetAllDomainsUseCase]
):
    """Получить список всех отслеживаемых доменов"""
    domains = await use_case.execute()
    return [
        DomainResponse(
            id=domain.id,
            url=domain.url,
            created_at=domain.created_at
        )
        for domain in domains
    ]


@router.get("/domains/{domain_id}/health", response_model=list[HealthCheckResponse])
async def get_domain_health(
        domain_id: int,
        use_case: FromDishka[GetDomainHealthUseCase],
        hours: int = 24,
):
    """Получить историю проверок домена за последние N часов"""
    try:
        checks = await use_case.execute(domain_id, hours)
        return [
            HealthCheckResponse(
                id=check.id,
                domain_id=check.domain_id,
                status_code=check.status_code,
                response_time=check.response_time,
                checked_at=check.checked_at,
                error_message=check.error_message,
                is_available=check.is_available
            )
            for check in checks
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
