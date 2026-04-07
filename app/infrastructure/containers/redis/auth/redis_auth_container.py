from dependency_injector import containers, providers

from app.application.redis.auth.use_cases.redis_auth_revoke_token_use_cases import RedisAuthRevokeTokenUseCase
from app.infrastructure.db.redis.redis_client import RedisClient
from app.infrastructure.repositories.redis.auth.redis_auth_repository import RedisAuthRepository
from app.settings import get_settings

settings = get_settings()

class RedisAuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "app.presentation.routes.auth.jwt.jwt_routes"
    ])

    redis_client = providers.Resource(RedisClient().get_redis_client)
    redis_auth_respository = providers.Factory(RedisAuthRepository, redis_client=redis_client)

    redis_auth_revoke_token_use_case = providers.Factory(
        RedisAuthRevokeTokenUseCase, 
        redis_auth_respository=redis_auth_respository
    )
