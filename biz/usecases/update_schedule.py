from pydantic import BaseModel, Field, constr, field_validator
from db.data import data
from utils.error.error_models import ErrorInfo
import re



class UpdateRequest(BaseModel):
    name: str = Field(..., title="The name of job", max_length=100, min_length=1, description="Schedule name")
    time: str = Field(..., description="Time in HH:MM format")
    weekday: str = Field(..., description="['Sunday', 'Monday', 'Tuesday'.. etc)]")

    @field_validator('name')
    def validate_job(cls, name):
        for job in data.job:
            if name == job.name:
                return name
        raise ValueError(ErrorInfo.job_not_found_error.message)
            

    @field_validator('time')
    def validate_time(cls, value):
        if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', value):
            raise ValueError(ErrorInfo.schedule_time_invalid.message)
        return value


    @field_validator("weekday")
    def validate_weekday(cls, value):
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "*"]

        if value.capitalize() not in weekdays:
            raise ValueError(ErrorInfo.weekdays_invalid.message)
        if value == "*":
            return value
        value = str(weekdays.index(value.capitalize()))
        return value


    def convert_time_to_cron_format(self):
        hour, minute = self.time.split(":")
        return f"{hour} {minute}"


    def schedule(self):
        clock = self.convert_time_to_cron_format()
        cron = str(f"{clock} * * {self.weekday}")
        return cron

class UpdateDataResponse(BaseModel):
    success: bool = Field(...)

class UpdateDataUseCase(BaseModel):
    async def handle(self, req: UpdateRequest) -> UpdateDataResponse:
        for job in data.job:
            if req.name == job.name:
                schedule = req.schedule()
                with open(job.jinja2_path, 'r') as file:
                    jinja2_content = file.read()
                jinja_content = jinja2_content.replace('{{ SCHEDULE_TIME }}', schedule)
                with open(f"{job.dag_output_locate}/{job.name}.py", "w") as f:
                    f.write(jinja_content)                      
                return UpdateDataResponse(success=True)
        raise RuntimeError(ErrorInfo.update_process)
