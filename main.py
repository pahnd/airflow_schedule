from fastapi import status, APIRouter, HTTPException, FastAPI
from biz.usecases.update_schedule import UpdateRequest, UpdateDataUseCase
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/v1/airflow/update")
async def schedule(request: UpdateRequest):
    try: 
        response = await UpdateDataUseCase().handle(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
