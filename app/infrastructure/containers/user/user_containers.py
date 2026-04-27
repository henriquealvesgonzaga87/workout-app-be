from dependency_injector import containers, providers

from app.application.user.use_cases.create_user_use_case import CreateUserUseCase
from app.application.user.use_cases.delete_user_use_case import DeleteUserUseCase
from app.application.user.use_cases.get_all_users_use_case import GetAllUsersUseCase
from app.application.user.use_cases.get_user_by_email_use_case import GetUserByEmailUseCase
from app.application.user.use_cases.get_user_by_id_use_case import GetUserByIdUseCase
from app.application.user.use_cases.update_user_use_case import UpdateUserUseCase
from app.infrastructure.db.sqlite.dependencies import get_db
from app.infrastructure.repositories.sqlalchemy.user.user_repo import SQLAlchemyUserRepository
from app.settings import get_settings

settings = get_settings()


class UserContainer(containers.DeclarativeContainer):
   wiring_config = containers.WiringConfiguration(modules=[
      "app.presentation.routes.user.user_routes"
   ])

   data_base_session = providers.Resource(get_db)
   user_repository = providers.Factory(SQLAlchemyUserRepository, db_session=data_base_session)

   create_user_use_case = providers.Factory(CreateUserUseCase, user_repository=user_repository)
   get_all_users_use_case = providers.Factory(GetAllUsersUseCase, user_repository=user_repository)
   get_user_by_id_use_case = providers.Factory(GetUserByIdUseCase, user_repository=user_repository)
   update_user_use_case = providers.Factory(UpdateUserUseCase, user_repository=user_repository)
   delete_user_use_case = providers.Factory(DeleteUserUseCase, user_repository=user_repository)
   get_user_by_email_use_case = providers.Factory(GetUserByEmailUseCase, user_repository=user_repository)
