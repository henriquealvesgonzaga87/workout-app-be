from app.presentation.error_handlers.error import Error


class DataBaseError(Error):
    def __init__(self, message: str):
        super().__init__(message)
