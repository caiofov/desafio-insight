import datetime
from fastapi import FastAPI, Request, Response

from app.routes.localidades import router as localidades_router
from app.routes.nomes import router as nomes_router
import uvicorn
import logging

app = FastAPI()

app.include_router(localidades_router, prefix="/localidades", tags=["Localidades"])
app.include_router(nomes_router, prefix="/nomes", tags=["Nomes"])

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
