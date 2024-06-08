import datetime
from fastapi import FastAPI, Request, Response

from app.routes.ibge import router as ibge_router
import uvicorn
import logging

app = FastAPI()

app.include_router(ibge_router, prefix="/ibge")

logger = logging.getLogger("uvicorn.info")


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = datetime.datetime.now()
    response: Response = await call_next(request)

    process_time = (datetime.datetime.now() - start_time).total_seconds()
    logger.info(f"Process time: {process_time}s")
    response.headers["X-Process-Time"] = str(process_time)

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
