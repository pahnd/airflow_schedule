from fastapi import APIRouter, HTTPException
from biz.usecases.update_schedule import UpdateRequest, UpdateDataUseCase
from utils.exception.exception_types import DataException

router = APIRouter()

@router.post("/schedule_update")
async def update_schedule(req:  UpdateRequest):
    try:
        response = UpdateDataUseCase().handle(req)
        return response
    except DataException  as e:
        raise HTTPException(status_code=404, detail=e.error_info)
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Invalid weekday name")
    except:
        raise HTTPException(status_code=500, detail="404 Not Found")
