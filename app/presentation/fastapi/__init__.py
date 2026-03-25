from app.presentation.fastapi.app import App
from app.settings import get_settings


settings = get_settings()
app = App.get_app(settings=settings)
