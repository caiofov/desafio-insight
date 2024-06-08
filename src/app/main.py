from fastapi import FastAPI

from app.router import router
import uvicorn

app = FastAPI()

app.include_router(router, prefix="/ibge")


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main___":
    uvicorn.run(app, port=5000, log_level="info")
