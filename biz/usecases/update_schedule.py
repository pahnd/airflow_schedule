from pydantic import BaseModel, Field, constr, field_validator
from db import data
from utils.exception.exception_types import DataException 
from utils.error.error_models import ErrorInfo
from jinja2 import Environment
import re



class UpdateRequest(BaseModel):
    name: str = Field(..., title="The name of job", max_length=100, min_length=1)
    time: str = Field(..., description="Time in HH:MM format")
    weekday: str = constr(min_length=1)

    @field_validator('time')
    def validate_time(cls, value):
        if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', value):
            raise ValueError("Invalid time format. Time must be in HH:MM format.")
        return value


    @field_validator("weekday")
    def validate_weekday(cls, value):
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "*"]

        if value.capitalize() not in weekdays:
            raise ValueError("Invalid request value: Weekday")
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
                schedule = {'SCHEDULE': req.schedule()}
                with open(job.jinja2_path, 'r') as file:
                    jinja2_content = file.read()
                env = Environment()
                template = env.from_string(jinja2_content)
                with open(f"{job.dag_output_locate}/{job.name}.py", "w") as f:
                    f.write(template.render(schedule))       
                return UpdateDataResponse(success=True)
        raise DataException(error_info=ErrorInfo.job_not_found_error)

