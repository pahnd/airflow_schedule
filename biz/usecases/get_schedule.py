from db.data import data
from typing import List
from pydantic import BaseModel, Field


class GetAllDataResponse(BaseModel):
    name: str = Field(...)

class GetDataUseCase(BaseModel):
    async def handle(self) -> List[GetAllDataResponse]:
        response = []
        for job in data.job:
            response.append(GetAllDataResponse(name=job.name))
        return response