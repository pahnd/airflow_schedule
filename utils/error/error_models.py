from pydantic import BaseModel


class ErrorInfoModel:
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __repr__(self):
        return f'code:{self.code},message:{self.message}'


class ErrorInfo:
    job_not_found_error = ErrorInfoModel(code=400, message='Name schedule not found')


class ErrorResponseModel(BaseModel):
    error_code: int = None
    error_message: str = None
    error_detail: list = None