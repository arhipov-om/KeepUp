from datetime import datetime, timedelta

import jwt
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from keep_up.application.services.user_service import UserService
from keep_up.domain.entities.user import User

bearer_scheme = HTTPBearer()

# TODO: заменить на RS256, вынести в конфиг.
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


class JWTHelper:
    @staticmethod
    def encode(user_uuid: str, username: str) -> str:
        data = {
            "sub": user_uuid,
            "username": username,
            "exp": datetime.now() + timedelta(hours=1),
        }
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode(token: str | bytes):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


@inject
async def get_current_user(
    user_service: FromDishka[UserService],
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:
    try:
        payload = JWTHelper.decode(credentials.credentials)
        user_uuid: str = payload.get("sub")
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )
    if user_uuid is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )
    return await user_service.get_user(user_uuid=user_uuid)
