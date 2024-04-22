from pydantic import BaseModel, Field, constr, field_validator
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from db import data
from utils.exception.exception_types import DataException 
from utils.error.error_models import ErrorInfo

import yaml

from jinja2 import Environment

class UpdateRequest(BaseModel, BaseRequest):
    name: str = Field("", title="The name of job", max_length=100, min_length=1)
    time: str = constr(pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    weekday: constr(min_length=1)
    
    @field_validator("weekday")
    def validate_weekday(cls, weekday):
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "*"]

        if weekday.capitalize() not in weekdays:
            raise ValueError("Invalid request value: Weekday")

        try:
            if weekday == "*":
                return weekday
            return str(weekdays.index(weekday.capitalize()))
        except ValueError:
            raise ValueError("Invalid weekday name")
    

    def convert_time_to_cron_format(self):
        hour, minute = self.time.split(":")
        return f"{minute} {hour}"


    def schedule(self):
        clock = self.convert_time_to_cron_format(self)
        cron = str(f"{clock} * * {self.weekday}")
        return cron




class UpdateDataResponse(BaseModel, BaseResponse):
    success: bool = Field(...)

class UpdateDataUseCase(BaseHandler):
    async def handle(self, req: UpdateRequest) -> UpdateDataResponse:
        for job in data.job:
            if req.name == job.name:
                with open(job.path_file, 'r') as file:
                    jinja2_content = file.read()

                env = Environment()
                template = env.from_string(jinja2_content)

                with open(f"{job.config_schedule_file}", "r") as input_file:
                    inputs = yaml.safe_load(input_file)
                    with open(f"{job.dag_output_locate}/{job.name}.py", "w") as f:
                        f.write(template.render(inputs))

                file_path == job.jinja2_path
                req.schedule 
                
                return UpdateDataResponse(success=True)
        raise DataException(error_info=ErrorInfo.job_not_found_error)

