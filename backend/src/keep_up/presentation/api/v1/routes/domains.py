from uuid import UUID

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from keep_up.application.use_cases.domain_use_cases import (
    AddDomainUseCase,
    GetDomainHealthUseCase,
    GetAllDomainsUseCase,
)
from keep_up.domain.exceptions import DomainAlreadyExistsError
from keep_up.presentation.api.v1.schemas import (
    AddDomainRequest,
    DomainResponse,
    HealthCheckResponse,
)
from keep_up.presentation.api.v1.utils import get_current_user

router = APIRouter(prefix="/domains", tags=["domains"], route_class=DishkaRoute)


@router.post(
    "/",
    response_model=DomainResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["secured"],
)
async def add_domain(
    request: AddDomainRequest,
    use_case: FromDishka[AddDomainUseCase],
    current_user=Depends(get_current_user),
):
    """Добавить новый домен для мониторинга"""
    try:
        domain = await use_case.execute(user_uuid=current_user.uuid, url=request.url)
        return DomainResponse(
            uuid=domain.uuid,
            url=domain.url,
            created_at=domain.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DomainAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", response_model=list[DomainResponse])
async def get_all_domains(use_case: FromDishka[GetAllDomainsUseCase]):
    """Получить список всех отслеживаемых доменов"""
    domains = await use_case.execute()
    return [
        DomainResponse(uuid=domain.uuid, url=domain.url, created_at=domain.created_at)
        for domain in domains
    ]


@router.get("/{domain_uuid}/health", response_model=list[HealthCheckResponse])
async def get_domain_health(
    domain_uuid: UUID,
    use_case: FromDishka[GetDomainHealthUseCase],
    hours: int = 24,
):
    """Получить историю проверок домена за последние N часов"""
    try:
        checks = await use_case.execute(domain_uuid, hours)
        return [
            HealthCheckResponse(
                uuid=check.uuid,
                domain_uuid=check.domain_uuid,
                status_code=check.status_code,
                response_time=check.response_time,
                checked_at=check.checked_at,
                error_message=check.error_message,
                is_available=check.is_available,
            )
            for check in checks
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
