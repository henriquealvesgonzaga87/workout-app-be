import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

from app.presentation.error_handlers.not_found_error import NotFoundError
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError

load_dotenv()

bearer_schema = HTTPBearer(auto_error=False)


def login_required(
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_schema)],
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
):
    if access_token is None:
        raise UnauthorizedError("Missing Authorization header: WWW-Authenticate: Bearer")

    access_token_data = access_token.credentials
    refresh_token_data = refresh_token

    try:
        access_token_payload = jwt.decode(
            token=access_token_data,
            key=os.getenv("SECRET_KEY"),
            algorithms=os.getenv("ALGORITHM"),
        )

        access_token_id: int | None = access_token_payload.get("id")
        access_token_role: bool | None = access_token_payload.get("role")
        access_token_user_state: bool | None = access_token_payload.get("is_active")

        if access_token_id is None:
            raise JWTError(f"{access_token_id} not valid")

        refresh_token_payload = jwt.decode(
            token=refresh_token_data,
            key=os.getenv("REFRESH_SECRET_KEY"),
            algorithms=os.getenv("ALGORITHM"),
        )

        refresh_token_id: int | None = refresh_token_payload.get("id")
        refresh_token_user_state: bool | None = access_token_payload.get("is_active")

        if access_token_user_state is False or refresh_token_user_state is False:
            raise NotFoundError("User not registered. Please register and then login")

        if refresh_token_id is None:
            raise JWTError(f"{refresh_token_id} not valid")

        if (refresh_token_id != access_token_id) and access_token_role is False:
            raise UnauthorizedError("You don't have authorization for this operation!")

        return access_token_payload

    except ExpiredSignatureError:
        raise UnauthorizedError("Access-token expired. WWW-Authenticate: Bearer")

    except JWTError as e:
        raise UnauthorizedError(f"Invalid Token. WWW-Authenticate: Bearer. !!!{e}")
