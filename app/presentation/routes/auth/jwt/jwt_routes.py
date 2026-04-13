import os

from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends, Header, status
from fastapi.encoders import jsonable_encoder

from app.domain.user.entities import User
from app.infrastructure.containers.auth.jwt.jwt_conatiners import JwtAuthContainer
from app.infrastructure.containers.redis.auth.redis_auth_container import RedisAuthContainer
from app.presentation.mappers.auth.jwt.mappers import JwtMapper
from app.presentation.models.auth.jwt.jwt_models import JwtLoginRequest, JwtTokenSchemaResponse
from app.presentation.routes.auth.jwt.jwt_dependencies import login_required

load_dotenv()


router = APIRouter(
    tags=["jwt_auth"],
    prefix="/jwt-auth"
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=JwtTokenSchemaResponse)
@inject
def login(
    login_data: JwtLoginRequest = Body(...),
    jwt_auth_login_use_cases = Depends(Provide[JwtAuthContainer.jwt_login_user_case])
):
    input_dto = JwtMapper.to_application_dto(jwt_request_data=login_data)
    output_dto = jwt_auth_login_use_cases.execute(input_dto)

    output_dto_response = JwtMapper.to_web_response(output_dto)

    return jsonable_encoder(output_dto_response)

@router.get("/refresh", status_code=status.HTTP_200_OK, response_model=JwtTokenSchemaResponse)
@inject
def refresh_token(
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    current_user: User = Depends(login_required),
    jwt_auth_refresh_token_use_cases = Depends(Provide[JwtAuthContainer.jwt_refresh_token_use_case])
):
    refreshed_token = jwt_auth_refresh_token_use_cases.execute(refresh_token=refresh_token)

    output_dto_response = JwtMapper.to_web_response(jwt_output_dto=refreshed_token)

    return jsonable_encoder(output_dto_response)

@router.get("/logout", status_code=status.HTTP_200_OK)
@inject
def logout(
    refresh_token: str = Header(..., alias="X-Refresh-Token"),
    current_user: User = Depends(login_required),
    redis_auth_revoke_token_use_case = Depends(Provide[RedisAuthContainer.redis_auth_revoke_token_use_case])
):
    revoke_token = redis_auth_revoke_token_use_case.execute(
        refresh_token=refresh_token,
        expires_in=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    )

    response = {"revoked": revoke_token}

    return jsonable_encoder(response)
