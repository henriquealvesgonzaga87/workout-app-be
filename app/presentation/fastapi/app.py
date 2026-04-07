from starlette.middleware.cors import CORSMiddleware

from app.infrastructure.containers.auth.jwt.jwt_conatiners import JwtAuthContainer
from app.infrastructure.containers.redis.auth.redis_auth_container import RedisAuthContainer
from app.infrastructure.containers.user.user_containers import UserContainer
from app.presentation.error_handlers.atribute_error import AttributeError
from app.presentation.error_handlers.bad_request_error import BadRequestError
from app.presentation.error_handlers.data_base_error import DataBaseError
from app.presentation.error_handlers.error_handler import ErrorHandler
from app.presentation.error_handlers.integrity_error import IntegrityError
from app.presentation.error_handlers.not_found_error import NotFoundError
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError
from app.presentation.error_handlers.type_error import TypeError as CustomTypeError
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError
from app.presentation.routes.auth.jwt import jwt_routes
from app.presentation.routes.user import user_routes
from app.settings import Settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class App:
    def __init__(self, settings: Settings):
        self.user_container: UserContainer = UserContainer()
        self.jwt_auth_container: JwtAuthContainer = JwtAuthContainer()
        self.redis_auth_container: RedisAuthContainer = RedisAuthContainer()
        self.user_container.init_resources()
        self.user_container.wire(modules=["app.presentation.routes.user.user_routes"])
        self.jwt_auth_container.wire(modules=["app.presentation.routes.auth.jwt.jwt_routes"])
        self.redis_auth_container.wire(modules=["app.presentation.routes.auth.jwt.jwt_routes"])

        self.app = FastAPI(title=settings.PROJECT_NAME, root_path=settings.ROOT_PATH)
        self.app.include_router(user_routes.router, prefix=settings.PREFIX)
        self.app.include_router(jwt_routes.router, prefix=settings.PREFIX)

        origins = ['*']

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

        @self.app.exception_handler(ResponseError)
        def response_error(request: Request, exc: ResponseError) -> JSONResponse:
            return ErrorHandler.response_error_handler(request=request, exc=exc)

        @self.app.exception_handler(RequestError)
        def request_error(request: Request, exc: RequestError) -> JSONResponse:
            return ErrorHandler.request_error_handler(request=request, exc=exc)

        @self.app.exception_handler(IntegrityError)
        def integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
            return ErrorHandler.integrity_error_handler(request=request, exc=exc)

        @self.app.exception_handler(DataBaseError)
        def data_base_error(request: Request, exc: DataBaseError) -> JSONResponse:
            return ErrorHandler.data_base_error_handler(request=request, exc=exc)

        @self.app.exception_handler(NotFoundError)
        def not_found_error(request: Request, exc: NotFoundError) -> JSONResponse:
            return ErrorHandler.not_found_error_handler(request=request, exc=exc)

        @self.app.exception_handler(AttributeError)
        def attribute_error(request: Request, exc: AttributeError) -> JSONResponse:
            return ErrorHandler.attribute_error_handler(request=request, exc=exc)

        @self.app.exception_handler(UnauthorizedError)
        def unauthorized_error(request: Request, exc: UnauthorizedError) -> JSONResponse:
            return ErrorHandler.unauthorized_error_handler(request=request, exc=exc)

        @self.app.exception_handler(CustomTypeError)
        def type_error_error(request: Request, exc: CustomTypeError) -> JSONResponse:
            return ErrorHandler.type_error_error_handler(request=request, exc=exc)

        @self.app.exception_handler(BadRequestError)
        def bad_request_error(request: Request, exc: BadRequestError) -> JSONResponse:
            return ErrorHandler.bad_request_error_handler(request=request, exc=exc)

    @classmethod
    def get_app(cls, settings: Settings) -> FastAPI:
        app_instance = cls(settings=settings)
        return app_instance.app
