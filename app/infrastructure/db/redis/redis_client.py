import redis

from app.settings import get_settings


class RedisClient:

    def __init__(self):
        settings = get_settings()
        self.host = settings.REDIS_HOST
        self.port = settings.REDIS_PORT
        self.db = settings.REDIS_DB
        self.decode_responses = settings.REDIS_DECODE_RESPONSES

    def _create_redis_client(self, host, port, db, decode_responses):
        return redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses
        )

    def get_redis_client(self):
        client = self._create_redis_client(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=self.decode_responses
        )
        try:
            yield client
        finally:
            client.close()
            client.connection_pool.disconnect()
