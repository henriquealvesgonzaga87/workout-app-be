from fastapi import status, Request
from fastapi.responses import JSONResponse
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError
from app.presentation.error_handlers.integrity_error import IntegrityError


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
