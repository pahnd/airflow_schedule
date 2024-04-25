from pydantic import BaseModel, field_validator
from typing import List, Dict
from os import path


class Job(BaseModel):
    name: str
    template_path: str
    dag_output_locate: str

    @field_validator("jinja2_path")
    def check_jinja_path_exist(cls, jinja2_path):
        if not path.exists(jinja2_path):
            raise ValueError(f"File path '{jinja2_path}' does not exist")
        return jinja2_path

    @field_validator("dag_output_locate")
    def check_directory_dag(cls, dag_output_locate):
        if not path.isdir(dag_output_locate):
            raise ValueError(f"Directory  path '{dag_output_locate}' does not exist")
        return dag_output_locate

class JobDict(BaseModel):
    job: List[Job]

def NewJobDict(data: dict()) -> JobDict:
    filtered_jobs = JobDict(job=[])
    for job_data in data['job']:
        job = Job(**job_data)
        filtered_jobs.job.append(job)
    return filtered_jobs
