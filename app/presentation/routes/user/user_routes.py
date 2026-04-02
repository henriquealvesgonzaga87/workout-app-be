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
)

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
    get_all_users_case = Depends(Provide[UserContainer.get_all_users_use_case])
):
    users = get_all_users_case.execute()

    users_dto_response = UserMapper.to_web_response(users)

    return jsonable_encoder(users_dto_response)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CreateUserResponse)
@inject
def get_user_by_id(
    id: int,
    get_user_by_id_use_case = Depends(Provide[UserContainer.get_user_by_id_use_case])
):
    user = get_user_by_id_use_case.execute(id=id)

    user_dto_response = UserMapper.to_web_response(user)

    return jsonable_encoder(user_dto_response)
