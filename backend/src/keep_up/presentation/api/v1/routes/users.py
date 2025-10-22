from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from keep_up.application.services.user_service import UserService
from keep_up.domain.exceptions import UserConflictError
from keep_up.presentation.api.v1.schemas import (
    RegisterUserRequest,
    LoginUserRequest,
    RegisterUserResponse,
    LoginUserResponse,
)
from keep_up.presentation.api.v1.utils import get_current_user, JWTHelper

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.post(
    "/register",
    response_model=RegisterUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
)
async def register(
    request: RegisterUserRequest,
    service: FromDishka[UserService],
) -> RegisterUserResponse:
    try:
        user = await service.register_user(
            username=request.username, email=request.email, password=request.password
        )
        return RegisterUserResponse(
            uuid=user.uuid, username=user.username, email=user.email
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except UserConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.args[0])


@router.post(
    "/login",
    response_model=LoginUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
    },
)
async def login(
    request: LoginUserRequest,
    service: FromDishka[UserService],
):
    user = await service.login_user(
        username=request.username, password=request.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = JWTHelper.encode(user_uuid=str(user.uuid), username=user.username)
    return LoginUserResponse(
        uuid=user.uuid,
        username=user.username,
        email=user.email,
        token=access_token,
    )


@router.get(
    "/me",
    tags=["secured"],
)
async def read_me(current_user: dict = Depends(get_current_user)):
    print(current_user)
    return
