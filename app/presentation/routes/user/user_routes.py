from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from app.infrastructure.containers.user.user_containers import UserContainer
from app.presentation.error_handlers.request_error import RequestError
from app.presentation.mappers.user.mappers import UserMapper
from app.presentation.models.user.create_user_model import (
    CreateUserRequest,
    CreateUserResponse,
    UpdateUserRequest,
)
from app.presentation.routes.auth.jwt.jwt_dependencies import login_required

router = APIRouter(
    tags=["user"],
    prefix="/user"
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
@inject
def create(
    request_data: CreateUserRequest = Body(...),
    create_user_use_case = Depends(Provide[UserContainer.create_user_use_case])
):
    try:
        input_dto = UserMapper.to_application_dto(request_data)
        output_dto = create_user_use_case.execute(input_dto)

        output_dto_response = UserMapper.to_web_response(output_dto)

        return jsonable_encoder(output_dto_response)
    except RequestValidationError as e:
        raise RequestError(f"Unable to proccess the request {e}")

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CreateUserResponse])
@inject
def get_all_users(
    get_all_users_case = Depends(Provide[UserContainer.get_all_users_use_case]),
    access_token_payload: dict[str, Any] = Depends(login_required),
):
    users = get_all_users_case.execute(access_token_payload=access_token_payload)

    users_dto_response = UserMapper.to_web_response(users)

    return jsonable_encoder(users_dto_response)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CreateUserResponse)
@inject
def get_user_by_id(
    id: int,
    get_user_by_id_use_case = Depends(Provide[UserContainer.get_user_by_id_use_case]),
    access_token_payload: dict[str, Any] = Depends(login_required),
):
    user = get_user_by_id_use_case.execute(id=id, access_token_payload=access_token_payload)

    user_dto_response = UserMapper.to_web_response(user)

    return jsonable_encoder(user_dto_response)

@router.patch("/{id}", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
@inject
def update(
    id: int,
    user_data: UpdateUserRequest = Body(...),
    access_token_payload: dict[str, Any] = Depends(login_required),
    update_user_use_case = Depends(Provide[UserContainer.update_user_use_case])
):
    input_dto = UserMapper.to_application_dto_update(user_request_data=user_data)
    update_user = update_user_use_case.execute(
        id=id,
        user_dto=input_dto,
        access_token_payload=access_token_payload
    )

    output_dto_response = UserMapper.to_web_response(update_user)

    return jsonable_encoder(output_dto_response)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete(
    id: int,
    delete_user_use_case = Depends(Provide[UserContainer.delete_user_use_case]),
    access_token_payload: dict[str, Any] = Depends(login_required),
):
    delete_user_use_case.execute(id=id, access_token_payload=access_token_payload)

    return True
