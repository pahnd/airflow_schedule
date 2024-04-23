from fastapi import FastAPI
from biz.usecases.update_schedule import UpdateRequest, UpdateDataUseCase
import uvicorn
from handler.api.update_schedule_handler import router

app = FastAPI()


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
