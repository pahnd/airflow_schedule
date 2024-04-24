from pydantic import BaseModel


class ErrorInfoModel:
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __repr__(self):
        return f'code:{self.code},message:{self.message}'


class ErrorInfo:
    job_not_found_error = ErrorInfoModel(code=400, message='Invalid request value: Name schedule not found')
    schedule_time_invalid = ErrorInfoModel(code=400, message='"Invalid request value: Invalid time format. Time must be in HH:MM format."')
    weekdays_invalid = ErrorInfoModel(code=400, message='Invalid request value: Weekday must be ["Sunday", "Monday", "Tuesday", etc..')
    update_process = ErrorInfoModel(code=500, message="Internal handler error: Can't modify jinja Schedule")