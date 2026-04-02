from abc import ABC, abstractmethod

from app.domain.user.entities import User


class UserInterface(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> User:
        pass
