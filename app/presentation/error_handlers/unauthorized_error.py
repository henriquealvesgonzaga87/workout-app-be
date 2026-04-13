from app.presentation.error_handlers.error import Error


class UnauthorizedError(Error):
    def __init__(self, message: str):
        super().__init__(message)
