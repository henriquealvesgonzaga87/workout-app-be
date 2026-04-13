from abc import ABC, abstractmethod


class RedisAuthRepositoryInterface(ABC):

    @abstractmethod
    def revoke_refresh_token(self, refresh_token: str, expires_in: int) -> bool:
        pass

    @abstractmethod
    def is_refresh_token_revoked(self, refresh_token: str) -> None:
        pass
