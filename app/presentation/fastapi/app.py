from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.settings import Settings


class App:
    def __init__(self, settings: Settings):
        self.app = FastAPI(title=settings.PROJECT_NAME, root_path=settings.ROOT_PATH)

        origins = ['*']

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    @classmethod
    def get_app(cls, settings: Settings) -> FastAPI:
        app_instance = cls(settings=settings)
        return app_instance.app
