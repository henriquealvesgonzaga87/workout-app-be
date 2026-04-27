from dependency_injector import containers, providers

from app.application.auth.jwt.use_cases.jwt_login_use_case import JwtLoginUseCases
from app.application.auth.jwt.use_cases.jwt_referesh_token_use_case import JwtRefreshTokenUseCases
from app.infrastructure.auth.jwt.jwt_handler import JwtHandler
from app.infrastructure.db.redis.redis_client import RedisClient
from app.infrastructure.db.sqlite.dependencies import get_db
from app.infrastructure.repositories.redis.auth.redis_auth_repository import RedisAuthRepository
from app.infrastructure.repositories.sqlalchemy.user.user_repo import SQLAlchemyUserRepository
from app.settings import get_settings

settings = get_settings()


class JwtAuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "app.presentation.routes.auth.jwt.jwt_routes"
    ])

    data_base_session = providers.Resource(get_db)
    redis_client = providers.Resource(RedisClient().get_redis_client)

    user_repository = providers.Factory(SQLAlchemyUserRepository, db_session=data_base_session)
    redis_auth_respository = providers.Factory(RedisAuthRepository, redis_client=redis_client)
    jwt_handler = providers.Factory(
        JwtHandler, 
        user_repository=user_repository,
        redis_auth_respository=redis_auth_respository
    )

    jwt_login_user_case = providers.Factory(
        JwtLoginUseCases,
        jwt_handler=jwt_handler,
        user_repository=user_repository
    )
    jwt_refresh_token_use_case = providers.Factory(JwtRefreshTokenUseCases, jwt_handler=jwt_handler)
