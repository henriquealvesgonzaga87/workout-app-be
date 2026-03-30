from app.presentation.error_handlers.error import Error


class RequestError(Error):
    def __init__(self, message: str):
        super().__init__(message)
