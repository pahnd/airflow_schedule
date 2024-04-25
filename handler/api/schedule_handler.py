from fastapi import APIRouter, HTTPException
from biz.usecases.update_schedule import UpdateRequest, UpdateDataUseCase
from biz.usecases.get_schedule import GetDataUseCase

router = APIRouter()

@router.post("/v1/schedule_update")
async def update_schedule(req:  UpdateRequest):
    try:
        response = UpdateDataUseCase().handle(req)
        return await response
    except Exception  as err:
        print(err)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")

@router.get("/v1/schedules")
async def get_schedule():
    try:
        response = GetDataUseCase().handle()
        return await response
    except Exception  as err:
        print(err)
        raise HTTPException(status_code=500, detail=f"Internal Server Error")