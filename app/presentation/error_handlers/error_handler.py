from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.presentation.error_handlers.atribute_error import AttributeError
from app.presentation.error_handlers.bad_request_error import BadRequestError
from app.presentation.error_handlers.data_base_error import DataBaseError
from app.presentation.error_handlers.forbidden_error import ForbiddenError
from app.presentation.error_handlers.integrity_error import IntegrityError
from app.presentation.error_handlers.not_found_error import NotFoundError
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError
from app.presentation.error_handlers.type_error import TypeError as CustomTypeError


class ErrorHandler:
    @staticmethod
    def response_error_handler(request: Request, exc: ResponseError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)}
        )

    @staticmethod
    def request_error_handler(request: Request, exc: RequestError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)}
        )

    @staticmethod
    def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(exc)}
        )

    @staticmethod
    def data_base_error_handler(request: Request, exc: DataBaseError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": str(exc)}
        )

    @staticmethod
    def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)}
        )

    @staticmethod
    def attribute_error_handler(request: Request, exc: AttributeError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": str(exc)}
        )

    @staticmethod
    def unauthorized_error_handler(request: Request, exc: AttributeError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)}
        )

    @staticmethod
    def type_error_error_handler(request: Request, exc: CustomTypeError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)}
        )

    @staticmethod
    def bad_request_error_handler(request: Request, exc: BadRequestError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)}
        )

    @staticmethod
    def forbidden_error_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": str(exc)}
        )
