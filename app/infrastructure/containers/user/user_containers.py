from dependency_injector import containers, providers
from app.application.user.use_cases.create_user_use_case import CreateUserUseCase
from app.infrastructure.repositories.sqlalchemy.user.user_repo import SQLAlchemyUserRepository
from app.infrastructure.repositories.dependencies import get_db
from app.settings import get_settings


settings = get_settings()


class UserContainer(containers.DeclarativeContainer):
   wiring_config = containers.WiringConfiguration(modules=[
      "app.presentation.routes.user.user_routes"
   ])

   data_base_session = providers.Resource(get_db)
   user_repository = providers.Factory(SQLAlchemyUserRepository, db_session=data_base_session)

   create_user_use_case = providers.Factory(CreateUserUseCase, user_repository=user_repository)
