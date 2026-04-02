from app.presentation.error_handlers.error import Error


class NotFoundError(Error):
    def __init__(self, message: str):
        super().__init__(message)
